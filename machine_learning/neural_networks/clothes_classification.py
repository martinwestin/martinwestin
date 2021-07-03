from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt


# loading the dataset
data = keras.datasets.fashion_mnist

# splitting the data --> 90% for training, 10% for testing
(train_images, train_labels), (test_images, test_labels) = data.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']


train_images = train_images / 255.0
test_images = test_images / 255.0

model = keras.Sequential([
    # flattened input layer with total length of 784
    keras.layers.Flatten(input_shape=(28,28)),
    # a dense layer, which means that it is fully connected. this is the hidden layer.
    # 128 - the length (amount of nodes/neurons) --> you usually want to use about 15 - 20% of the input size.
    # activation --> an activation function, which is a non-linear function
    # that allows us to add more complexity to the network
    # "relu" --> rectified linear unit: very fast activation function, works well in many cases.
    keras.layers.Dense(128, activation="relu"),
    # another dense layer, with 10 nodes/neurons. this is the output layer.
    # it has 10 nodes/neurons because we have 10 image classes.
    # "softmax" --> pick values for each output node/neuron, so that they all add up to 1.
    # it is the probability of the network thinking it is a specific value/output.
    keras.layers.Dense(10, activation="softmax")
])

# "adam" is typically the standard optimizer.
# metrics["accuracy"] --> defines what we are looking for when testing the model (accuracy/how low we can get the loss function to be).
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# epochs --> how many times the network will train on/see the same image.
# a way to hopefully increase the accuracy of the model.
model.fit(train_images, train_labels, epochs=5)

prediction = model.predict(test_images)
for i in range(5):
    plt.grid(False)
    plt.imshow(test_images[i], cmap=plt.cm.binary)
    plt.xlabel(f"Actual: {class_names[test_labels[i]]}")
    plt.title(f"Prediction: {class_names[np.argmax(prediction[i])]}")
    plt.show()
