import os
import sys
import tempfile
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from train import load_and_validate_data, get_models, pick_best_model, export_onnx, REQUIRED_COLUMNS


def create_temp_csv(data_dict):
    df = pd.DataFrame(data_dict)
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    df.to_csv(tmp.name, index=False)
    return tmp.name


def test_load_and_validate_data_success():
    path = create_temp_csv({
        'hours': [5, 7],
        'attendance': [80, 90],
        'previous_marks': [60, 70],
        'final_marks': [65, 78],
    })
    data = load_and_validate_data(path)
    assert len(data) == 2
    assert list(data.columns) == ['hours', 'attendance', 'previous_marks', 'final_marks']
    os.unlink(path)


def test_load_and_validate_data_missing_file():
    try:
        load_and_validate_data("/nonexistent/path.csv")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass


def test_load_and_validate_data_missing_columns():
    path = create_temp_csv({'hours': [5], 'attendance': [80]})
    try:
        load_and_validate_data(path)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    os.unlink(path)


def test_load_and_validate_data_null_values():
    path = create_temp_csv({
        'hours': [5, None],
        'attendance': [80, 90],
        'previous_marks': [60, 70],
        'final_marks': [65, 78],
    })
    try:
        load_and_validate_data(path)
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    os.unlink(path)


def test_get_models():
    models = get_models()
    assert 'LinearRegression' in models
    assert 'RandomForest' in models
    assert 'GradientBoosting' in models


def test_pick_best_model_returns_string():
    rng = np.random.default_rng(42)
    X = rng.random((50, 3)).astype(np.float32)
    y = (X[:, 0] * 2 + X[:, 1] * 0.5 + X[:, 2] * 0.3 + 1).astype(np.float32)
    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    models = get_models()
    best = pick_best_model(models, X_train, X_test, y_train, y_test)
    assert isinstance(best, str)
    assert best in models


def test_export_onnx_creates_file():
    model = LinearRegression()
    X = np.array([[5, 80, 60], [7, 90, 70]], dtype=np.float32)
    y = np.array([65, 78], dtype=np.float32)
    model.fit(X, y)

    tmpdir = tempfile.mkdtemp()
    path = export_onnx(model, tmpdir)
    assert os.path.exists(path)
    assert os.path.getsize(path) > 0
    os.unlink(path)
    os.rmdir(tmpdir)


def test_model_predicts_within_bounds():
    model = LinearRegression()
    rng = np.random.default_rng(42)
    X = rng.random((100, 3)).astype(np.float32) * 100
    y = (X[:, 0] * 0.5 + X[:, 1] * 0.3 + X[:, 2] * 0.2 + 5).astype(np.float32)
    model.fit(X, y)

    pred = model.predict(np.array([[10, 80, 70]], dtype=np.float32))
    assert 0 <= pred[0] <= 100
