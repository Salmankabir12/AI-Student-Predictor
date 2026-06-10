import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import os
import sys
import json


REQUIRED_COLUMNS = {'hours', 'attendance', 'previous_marks', 'final_marks'}
TARGET_OPSET = 18
TEST_SIZE = 0.2


def load_and_validate_data(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Training data not found at {csv_path}")
    data = pd.read_csv(csv_path)
    if not REQUIRED_COLUMNS.issubset(data.columns):
        missing = REQUIRED_COLUMNS - set(data.columns)
        raise ValueError(f"Missing columns: {missing}")
    if data.isnull().any().any():
        raise ValueError("Dataset contains null values")
    return data


def get_models():
    return {
        'LinearRegression': LinearRegression(),
        'RandomForest': RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        'GradientBoosting': GradientBoostingRegressor(
            n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42
        ),
    }


def evaluate_model(name, model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
    print(f"\n{name}:")
    print(f"  R\u00b2: {r2:.4f}  |  MAE: {mae:.3f}  |  CV R\u00b2: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    return model, r2, mae


def pick_best_model(models, X_train, X_test, y_train, y_test):
    best_r2 = -float('inf')
    best_name = None
    for name, model in models.items():
        fitted, r2, _ = evaluate_model(name, model, X_train, X_test, y_train, y_test)
        if r2 > best_r2:
            best_r2 = r2
            best_name = name
    print(f"\nBest model: {best_name} (R\u00b2: {best_r2:.4f})")
    return best_name


def export_onnx(model, output_dir):
    feature_names = ['hours', 'attendance', 'previous_marks']
    initial_type = [('float_input', FloatTensorType([None, len(feature_names)]))]
    onnx_model = convert_sklearn(model, initial_types=initial_type, target_opset=TARGET_OPSET)
    onnx_path = os.path.join(output_dir, "model.onnx")
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
    return onnx_path


def main():
    np.random.seed(42)
    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(OUTPUT_DIR, "student_data.csv")

    data = load_and_validate_data(csv_path)
    print(f"Dataset: {len(data)} rows, {len(data.columns)} columns")
    print(f"Features: {', '.join(data.columns)}")

    X = data[['hours', 'attendance', 'previous_marks']].values.astype(np.float32)
    y = data['final_marks'].values.astype(np.float32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=42)

    models = get_models()
    best_name = pick_best_model(models, X_train, X_test, y_train, y_test)

    final_model = models[best_name]
    final_model.fit(X, y)

    if best_name == 'LinearRegression':
        print(f"Coefficients: {list(final_model.coef_)}")
        print(f"Intercept: {final_model.intercept_}")
    else:
        importances = final_model.feature_importances_
        for name, imp in zip(['hours', 'attendance', 'previous_marks'], importances):
            print(f"  {name}: {imp:.4f}")

    onnx_path = export_onnx(final_model, OUTPUT_DIR)
    print(f"\nModel exported to {onnx_path}")
    print("Model training and export complete!")


if __name__ == "__main__":
    main()
