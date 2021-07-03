import tensorflow as tf
from tensorflow import keras
import numpy as np
import tkinter as tk


data = keras.datasets.imdb

(train_data, train_labels), (test_data, test_labels) = data.load_data(num_words=88000)

word_index = data.get_word_index()

# +3 because there are going to be 3 keys that are "special characters" for the word mapping.
word_index = {k:(v+3) for k, v in word_index.items()}

word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

reverse_word_index = dict([value, key] for key, value in word_index.items())

train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding="post", maxlen=250)
test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<PAD>"], padding="post", maxlen=250)

def decode(text):
    return " ".join([reverse_word_index.get(i, "?") for i in text])

# model

# model = keras.Sequential()
# model.add(keras.layers.Embedding(88000, 16))
# model.add(keras.layers.GlobalAveragePooling1D())
# model.add(keras.layers.Dense(16, activation="relu"))
# model.add(keras.layers.Dense(1, activation="sigmoid"))

# model.summary()
# model.compile(optimizer="adam", loss="binary_crossentropy")

# x_val = train_data[:10000]
# x_train = train_data[10000:]

# y_val = train_labels[:10000]
# y_train = train_labels[10000:]

# # batch_size --> how many reviews we are going to give to the model at once
# fit_model = model.fit(x_train, y_train, epochs=40, batch_size=512, validation_data=(x_val, y_val), verbose=1)

# model.save("machine_learning/neural_networks/text_classification/model.h5")

def review_encode(s):
    encoded = [1]
    for word in s:
        if word.lower() in word_index:
            encoded.append(word_index[word.lower()])
        else:
            encoded.append(2)
    
    return encoded


model = keras.models.load_model("machine_learning/neural_networks/text_classification/model.h5")
class_names = ["extremely negative", "very negative",
                "negative", "pretty negative", "a bit negative",
                "a bit positive", "pretty positive", "positive",
                "very positive", "extremely positive", "outstandingly positive"
            ]

with open("machine_learning/neural_networks/text_classification/review.txt", encoding="utf-8") as f:
    content = f.read()
    n_line = content.replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace(":", "").replace("\"", "").strip().split(" ")
    encode = review_encode(n_line)
    encode = keras.preprocessing.sequence.pad_sequences([encode], value=word_index["<PAD>"], padding="post", maxlen=250)
    predict = model.predict(encode)
    print(f"Review is {class_names[int(round(round(predict[0][0], 1) * 10))]}")
