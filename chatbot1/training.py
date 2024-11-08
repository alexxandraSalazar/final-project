import os
import json
import random
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Definir la ruta del directorio del modelo
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)) )

# Cargar los archivos generados en el código anterior
intents_file = os.path.join(model_path, 'intents.json')
words_file = os.path.join(model_path, 'words.pkl')
classes_file = os.path.join(model_path, 'classes.pkl')
model_file = os.path.join(model_path, 'chatbot_model.h5')

# Cargar los datos
with open(intents_file, 'r') as f:
    intents = json.load(f)

# Descargar los recursos necesarios de nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

words = []
classes = []
documents = []
ignore_letters = ['?', '!', '¿', '.', ',']

# Clasificar los patrones y las categorías
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
words = sorted(set(words))

# Guardar las palabras y las clases en archivos pickle
with open(words_file, 'wb') as f:
    pickle.dump(words, f)
with open(classes_file, 'wb') as f:
    pickle.dump(classes, f)

# Pasar la información a unos y ceros según las palabras presentes en cada categoría para hacer el entrenamiento
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
print(len(training))

train_x = []
train_y = []
for i in training:
    train_x.append(i[0])
    train_y.append(i[1])

train_x = np.array(train_x)
train_y = np.array(train_y)

# Crear la red neuronal
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Crear el optimizador y compilar el modelo
sgd = SGD(learning_rate=0.001, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Entrenar el modelo y guardarlo
model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=5, verbose=1)
model.save(model_file)
