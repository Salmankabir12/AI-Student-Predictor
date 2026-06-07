import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import pickle

data = pd.read_csv("student_data.csv")

X = data[['hours', 'attendance', 'previous_marks']]
y = data['final_marks']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"R² Score: {r2:.3f}")
print(f"MAE: {mae:.3f}")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")
