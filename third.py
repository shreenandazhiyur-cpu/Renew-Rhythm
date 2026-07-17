import serial
import multiprocessing as mp
import numpy as np
import pyttsx3
import time
import os
from tensorflow.keras.models import load_model

def ml_and_speaker_process(data_queue):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    
    if os.path.exists("renew_rhythm_model.h5"):
        model = load_model("renew_rhythm_model.h5")
    else:
        model = None

    words = ["hello", "water", "help", "yes", "no"]

    while True:
        if not data_queue.empty():
            sensor_window = data_queue.get()
            
            if model:
                sensor_window_reshaped = np.expand_dims(sensor_window, axis=0)
                prediction_idx = np.argmax(model.predict(sensor_window_reshaped))
                predicted_word = words[prediction_idx]
            else:
                predicted_word = "Model missing"

            print(f"Predicted: {predicted_word}")
            engine.say(predicted_word)
            engine.runAndWait()

def serial_reader_process(data_queue):
    ser = serial.Serial('COM3', 115200)
    time.sleep(2)
    
    word_buffer = []
    THRESHOLD = 2000
    SILENCE_DURATION = 30
    silence_counter = 0
    is_speaking = False
    FIXED_LENGTH = 100

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            vals = line.split(',')
            
            if len(vals) == 3:
                try:
                    j, m, a = int(vals[0]), int(vals[1]), int(vals[2])
                except ValueError:
                    continue
                
                if j > THRESHOLD or m > THRESHOLD:
                    is_speaking = True
                    silence_counter = 0
                    word_buffer.append([j, m, a])
                elif is_speaking:
                    silence_counter += 1
                    word_buffer.append([j, m, a])
                    
                    if silence_counter > SILENCE_DURATION:
                        is_speaking = False
                        
                        if len(word_buffer) > 20:
                            arr = np.array(word_buffer)
                            if len(arr) < FIXED_LENGTH:
                                pad_len = FIXED_LENGTH - len(arr)
                                arr = np.pad(arr, ((0, pad_len), (0, 0)), 'constant')
                            elif len(arr) > FIXED_LENGTH:
                                arr = arr[:FIXED_LENGTH]
                                
                            data_queue.put(arr)
                        
                        word_buffer = []

if __name__ == '__main__':
    q = mp.Queue()
    
    p1 = mp.Process(target=serial_reader_process, args=(q,))
    p2 = mp.Process(target=ml_and_speaker_process, args=(q,))
    
    p1.start()
    p2.start()
    
    p1.join()
    p2.join()
