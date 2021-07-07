"""
-- Copyright 2021. Dongwon Kim All rights reserved.
--
-- File name : Communication_func.py
-- 
-- Written by Dongwon Kim
--
-- Modbus TCP communication(header file)
--    connect to the server
--    get values from registers in server
--
-- Modificatoin history
--    written by Dongwon Kim on June 18, 2021
--
-- Encoding: UTF-8
--
"""

"""
Get local IP address
input
    none
output
    str server_ip: ip address of server to connect
    int server_port: port number(fixed to 502 for Modbus)
"""
def get_addr():    
    import socket

    hostname = socket.gethostname()
    server_ip_addr = socket.gethostbyname(hostname)
    server_port = 502

    return server_ip_addr, server_port

"""
Get value from server and return binary form string
input
    str server_ip: ip address of server to connect
    int server_port: port number(fixed t 502 for Modbus)
output
    return 16 bit binary str form of
        status  
        gas_info
        gas_value
        error_code
        units
        alarm1_limit
        alarm2_limit
"""
def get_value_from_server(server_ip, server_port):
    from pymodbus.client.sync import ModbusTcpClient
    
    #connect to the server
    client = ModbusTcpClient(server_ip, server_port)
    print("[+]Info : Connection" + str(client.connect()))

    #get values from server's registers
    #registers(0) = 40001
    #(start register's no., no. of regi to read)
    value = client.read_holding_registers(0, 16)
    
    #assign each values(int)
    status = value.registers[0]          #  40001
    gas_info = value.registers[1]        #  40002
    gas_value1 = value.registers[2]      #  40003
    gas_value2 = value.registers[3]      #  40004
    error_code = value.registers[5]      #  40006
    units = value.registers[6]           #  40007
    alarm1_limit1 = value.registers[12]  #  40013
    alarm1_limit2 = value.registers[13]  #  40014
    alarm2_limit1 = value.registers[14]  #  40015
    alarm2_limit2 = value.registers[15]  #  40016

    #change to binary form str
    #fix the length of str to 16 (1 word)
    status = padding(status, 16)
    gas_info = padding(gas_info, 16)
    gas_value1 = padding(gas_value1, 16)
    gas_value2 = padding(gas_value2, 16)
    gas_value = gas_value1 + gas_value2
    error_code = padding(error_code, 16)
    units = padding(units, 16)
    alarm1_limit1 = padding(alarm1_limit1, 16)
    alarm1_limit2 = padding(alarm1_limit2, 16)
    alarm1_limit = alarm1_limit1 + alarm1_limit2
    alarm2_limit1 = padding(alarm2_limit1, 16)
    alarm2_limit2 = padding(alarm2_limit2, 16)
    alarm2_limit = alarm2_limit1 + alarm2_limit2

    return status, gas_info, gas_value, error_code, units, alarm1_limit, alarm2_limit


"""
Change integer data to binary data
Fill remain part with 0 to make length to 'length'
input
    int data: decimal data to be converted in binary form
    int length: length to be made
output
    return str whose len is length, has binary value
"""
def padding(data, length):
    return bin(data)[2:].zfill(length)
