# Renew Rhythm

An open-source, machine-learning-powered augmentative and alternative communication (AAC) wearable prototype. Renew Rhythm translates subtle facial and mouth movements—specifically jaw motion, tongue movement, and airflow—into real-time communication using a custom piezoelectric sensor array.

# 🚀 Features

* **High-Sensitivity Sensor Array:** Utilizes 27mm piezoelectric discs mapped to specific facial muscle groups.
* **Custom Signal Processing:** Features a purpose-built 1.65V bias circuit to capture complete positive and negative AC waveforms from the piezo sensors without clipping.
* **Hardware Noise Reduction:** Implements shielded audio cables to eliminate ambient electrical interference (mains hum) before the data reaches the microcontroller.
* **Machine Learning Integration:** Processes raw analog telemetry into actionable, mapped communication outputs using Python-based ML scripts.
* **Hybrid Power Architecture:** Designed to operate via a portable power source, supported by a 5V TP4056-regulated solar docking station for sustainable, stationary charging.

# 🛠️ Hardware Stack

**Core Components:**
* Microcontroller: ESP32 Development Board
* Sensors: 27mm Piezoelectric Discs (Sensing and Energy Harvesting)
* Wiring: Shielded Audio Cable (Critical for analog noise isolation)

**Circuit & Protection:**
* Resistors: 22kΩ (Voltage divider/bias network), 1MΩ (Parallel bleed resistors)
* Protection: 5.1V Zener Diodes (C5V) for sensor channels, 1N4007 Silicon Diodes for microcontroller voltage regulation.
* Charging Dock: 5V Solar Panel, TP4056 Lithium Charging Module.

# 🔌 Circuit Architecture: The Hub & Spoke Model

The wearable prototype utilizes a "Hub and Spoke" design, where the processing unit (hub) is kept off-face, while the sensors (spokes) are routed via shielded cables.

The core of the sensing mechanism bypasses the ESP32's native inability to read negative voltages:
1. **The Bias Line:** Two 22kΩ resistors split the ESP32's 3.3V output to create a steady 1.65V reference line.
2. **Signal Lifting:** The ground of each sensing piezo is tied to this 1.65V bias rather than true ground. This lifts the AC audio/kinetic signal, allowing the ESP32's ADC pins to read the full physical waveform (both the push and the pull of the muscle).
3. **Hardware Protection:** 1MΩ resistors and Zener diodes run in parallel to the sensors to prevent physical impact spikes from overloading the ESP32's analog pins.

# 💻 Software & Setup

# Prerequisites
* Arduino IDE (for flashing the ESP32)
* Python 3.8+ (for data visualization and ML processing)
* Required Python libraries: `pyserial`, `matplotlib`, `numpy`, `scikit-learn`

# Running the Project
1. **Hardware:** Assemble the hub-and-spoke circuit according to the schematic. Ensure the 1.65V bias is stable before connecting the sensors.
2. **Firmware:** Flash the `data_collection.ino` script to the ESP32 to begin broadcasting analog readings over serial.
3. **Software:** Run `visualization.py` to monitor the real-time waveforms of the jaw, tongue, and airflow sensors. 

# 🏆 Acknowledgements

* Recognized for technical execution and design in regional collegiate technical exhibitions (1st and 2nd place honors). 

# 🔮 Future Roadmap
* Adding a dedicated Solar docking system , which could be used to further add to the fuel efficiency and to avoid a bulky setup in the wearable part.
* Transition from breadboard prototype to a miniaturized, wearable custom PCB.
* Expansion of the machine learning gesture library to support more complex communication arrays.
* Further optimization of the kinetic energy harvesting circuit.
