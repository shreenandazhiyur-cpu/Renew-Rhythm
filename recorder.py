import serial
import numpy as np
import time
import os

# --- Configuration ---
COM_PORT = 'COM3' 
BAUD_RATE = 115200 
FIXED_LENGTH = 100 
THRESHOLD = 2000 
SILENCE_DURATION = 30 
NUM_SENSORS = 3 

def record_word(target_word, num_samples=20): 
    # Open serial connection
    try:
        ser = serial.Serial(COM_PORT, BAUD_RATE) 
    except serial.SerialException as e:
        print(f"Error: Could not open {COM_PORT}. Check connection and close other apps.")
        return

    time.sleep(2) # Corrected from 'me.sleep'
    
    filename = f"{target_word}_data.csv" 
    
    for i in range(num_samples): 
        print(f"\nPrepare to say '{target_word}' (Sample {i+1}/{num_samples})") 
        time.sleep(1) # Corrected from 'me.sleep'
        print("Speak now!") 
        
        word_buffer = [] 
        is_speaking = False 
        silence_counter = 0 
        
        while True: 
            # Corrected spelling of 'in_waiting'
            if ser.in_waiting > 0: 
                line = ser.readline().decode('utf-8', errors='ignore').strip() 
                vals = line.split(',') 
                
                if len(vals) == NUM_SENSORS: 
                    try: 
                        j, m, a = int(vals[0]), int(vals[1]), int(vals[2]) 
                    except ValueError: 
                        continue 
                        
                    # Trigger recording when movement exceeds threshold
                    if j > THRESHOLD or m > THRESHOLD: 
                        is_speaking = True 
                        silence_counter = 0 
                        word_buffer.append([j, m, a]) 
                    elif is_speaking: 
                        silence_counter += 1 
                        word_buffer.append([j, m, a]) 
                        
                        # Stop recording after a period of silence
                        if silence_counter > SILENCE_DURATION: 
                            if len(word_buffer) > 20: 
                                arr = np.array(word_buffer) 
                                
                                # Pad or clip to fixed length for 1D-CNN input
                                if len(arr) < FIXED_LENGTH: 
                                    pad_len = FIXED_LENGTH - len(arr) 
                                    arr = np.pad(arr, ((0, pad_len), (0, 0)), 'constant') 
                                elif len(arr) > FIXED_LENGTH: 
                                    arr = arr[:FIXED_LENGTH] 
                                    
                                # Save data to CSV
                                with open(filename, 'a') as f: 
                                    # Corrected spelling of 'flatten'
                                    np.savetxt(f, arr.flatten()[np.newaxis], delimiter=",", fmt='%d') 
                                print("Saved.") 
                                break 
                            else: 
                                # Ignore accidental small movements
                                word_buffer = [] 
                                is_speaking = False 
    ser.close() 

if __name__ == '__main__': 
    # Switch to the 'Terminal' tab in VS Code to type this!
    word = input("Enter word to record (e.g., water): ").strip().lower() 
    record_word(word)