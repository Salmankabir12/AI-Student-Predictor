import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import os
import sys


REQUIRED_COLUMNS = {'hours', 'attendance', 'previous_marks', 'final_marks'}
TARGET_OPSET = 18


def main():
    np.random.seed(42)
    OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(OUTPUT_DIR, "student_data.csv")

    if not os.path.exists(csv_path):
        print(f"Error: training data not found at {csv_path}", file=sys.stderr)
        sys.exit(1)

    data = pd.read_csv(csv_path)

    if not REQUIRED_COLUMNS.issubset(data.columns):
        missing = REQUIRED_COLUMNS - set(data.columns)
        print(f"Error: missing columns in CSV: {missing}", file=sys.stderr)
        sys.exit(1)

    if data.isnull().any().any():
        print("Error: dataset contains null values", file=sys.stderr)
        sys.exit(1)

    X = data[['hours', 'attendance', 'previous_marks']].values.astype(np.float32)
    y = data['final_marks'].values.astype(np.float32)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print(f"Train/Test R\u00b2 Score: {r2:.3f}")
    print(f"Train/Test MAE: {mae:.3f}")

    final_model = LinearRegression()
    final_model.fit(X, y)

    print(f"Coefficients: {list(final_model.coef_)}")
    print(f"Intercept: {final_model.intercept_}")

    feature_names = ['hours', 'attendance', 'previous_marks']
    initial_type = [('float_input', FloatTensorType([None, len(feature_names)]))]
    onnx_model = convert_sklearn(final_model, initial_types=initial_type, target_opset=TARGET_OPSET)

    onnx_path = os.path.join(OUTPUT_DIR, "model.onnx")
    with open(onnx_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    print(f"Model exported to {onnx_path}")
    print("Model training and export complete!")


if __name__ == "__main__":
    main()
