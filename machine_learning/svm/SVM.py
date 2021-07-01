from sklearn import datasets
from sklearn import svm
import pickle

cancer = datasets.load_breast_cancer()

class Setup(svm.SVC):
    def __init__(self, kernel, C, **kwargs):
        """
        param kernel: the type of kernel to use.
        param C: how much of a soft margain you want to use.
        """
        super().__init__(kernel=kernel, C=C)
        self.fit(kwargs["x_train"], kwargs["y_train"])

data = pickle.load(open("machine_learning/svm/model", "rb"))
x_train, x_test, y_train, y_test = data[0], data[1], data[2], data[3]
classes = ['malignant', 'benign']
print("Features:\n", cancer.feature_names)

model = Setup("linear", 2, x_train=x_train, y_train=y_train)
model.fit(x_train, y_train)
predicted = model.predict(x_test)
for i in range(len(predicted)):
    print(f"Predicted case: {classes[predicted[i]]}", f"Actual case: {classes[y_test[i]]}")

def classify(case):
    """
    param case: a 2D list with structure [[attributes]]
    """
    return classes[model.predict(case)[0]]

new_case = [[]]
print("Predict new case")
for i in list(cancer.feature_names):
    try:
        new_case[0].append(float(input(f"{i}: ")))
    except:
        while True:
            print("Invalid input.")
            try:
                new_case[0].append(float(input(f"{i}: ")))
                break
            except:
                pass

print(f"Predicted: {classify(new_case)}")
