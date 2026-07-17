import numpy as np
import glob
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical

FIXED_LENGTH = 100
NUM_SENSORS = 3

X = []
y = []
label_map = {}

csv_files = glob.glob("*_data.csv")
for idx, file in enumerate(csv_files):
    word = file.replace("_data.csv", " ")
    label_map[idx] = word
    
    data = np.loadtxt(file, delimiter=",")
    if data.ndim == 1:
        data = data.reshape(1, -1)
        
    for row in data:
        X.append(row.reshape(FIXED_LENGTH, NUM_SENSORS))
        y.append(idx)

X = np.array(X)
y = to_categorical(np.array(y))

model = Sequential([
    Conv1D(32, kernel_size=3, activation='relu', input_shape=(FIXED_LENGTH, NUM_SENSORS)),
    MaxPooling1D(pool_size=2),
    Conv1D(64, kernel_size=3, activation='relu'),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(len(label_map), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=30, batch_size=8, validation_split=0.2)
model.save("renew_rhythm_model.h5")
print("Model saved! Labels:", label_map)
