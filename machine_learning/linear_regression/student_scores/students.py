import pandas as pd
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression

data = pd.read_csv("machine_learning/linear_regression/student_scores/student-mat.csv", sep=";")
data = data[["G1", "G2", "G3", "studytime", "failures", "absences"]]

predict = "G3"
x = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

model = LinearRegression()
model.fit(x_train, y_train)

predicted = model.predict(x_test)

for i in range(len(predicted)):
    print(f"Predicted: {predicted[i]}", f"Data: {x_test[i]}", f"Actual: {y_test[i]}")

print("ENTER NEW SCORES")
new = [[]]
for i in ["G1", "G2", "studytime", "failures", "absences"]:
    try:
        new[0].append(float(input(f"Enter {i}: ")))
    except:
        while True:
            print("Invalid input. Must be number.")
            try:
                new[0].append(float(input(f"Enter {i}: ")))
                break
            except:
                pass

new_prediction = model.predict(new)[0]
print(f"Predicted G3: {new_prediction}")
