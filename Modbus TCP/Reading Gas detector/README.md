# Purpose
- sample project using Modbus TCP protocol
- read data from gas detectors using Modbus TCP protocol

# How to run
1. run testing_server.ipynb
     - open local server
2. run testing_value.ipynb
     - write testing values to registers in server according to Gastron GTD-5000 address mapping sheet
3. run main.ipynb
     - connect to local server
     - get values from local server
     - interpret the values and print messages

# Output
- print decoded messages at console

# Prerequisite
- [Communication_func.py](./Communication_func.py), decoding.py and main.ipynb shold be in the same directory
- Run the code in an order noticed above
- Should install pymodbus by
-      pip install pymodbus

# Limitation
- Communication with Gas detector is not tested yet(2021.07.07)
