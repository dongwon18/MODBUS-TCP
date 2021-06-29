"""
-- Copyright 2021. Dongwon Kim All rights reserved.
--
-- File name : my_modbus.py
-- 
-- Written by Dongwon Kim
--    School of Electronic and Electrical Engineering
--
-- Modbus TCP communication
--    read multiple registers
--    write a single register
--
-- Modificatoin history
--    written by Dongwon Kim on June 29, 2021
"""
import socket
import struct
import time

"""
-- read multiple registers from server
--
-- input
--    int unitID: unitID(1byte) 
--    int addr: address of start register to be read(2byte)
--    int cnt: no. of registers to be read(2byte)
-- output
--    print sent packet
--    print recieved packet
-- prerequisite
--    addr should be givin such as 40001(not 0)
"""
def read_regi(unitID, addr, cnt):
    # read analog input regi
    if(int(addr / 10000) == 3):
        read_fcode = 4
    # read analog output holding regi
    elif(int(addr / 10000) == 4):
        read_fcode = 3

    if(addr > 10000):
        # to make 0 = 0x40001
        
        addr = int(addr % 10000) - 1
        print(addr)
    
    transID = 0
    protocolID = 0
    length = 6  #  len(unit) + len(fcode) + len(addr)  + len(cnt) = 1 + 1 + 2 + 2 = 6 byte

    #change to byte
    #Modbus: big endian(>), unsigned short(H, 2byte), unsigned byte(B)
    #transctionID(2byte) ProtocolID(2byte) length(2byte) unitID(1byte) Fcode(1byte) addr(2bytpe) cnt(2byte)    
    adu_read = struct.pack('>HHHBBHH', transID, protocolID, length, unitID, read_fcode, addr, cnt)
    print(adu_read)
    print('transID: ' + str(adu_read[0:2]))
    print('protoID: ' + str(adu_read[2:4]))
    print('length: ' + str(adu_read[4:6]))
    print('unit: ' + str(adu_read[6:7]))
    print('fcode: ' + str(adu_read[7:8]))
    print('addr: ' + str(adu_read[8:10]))
    print('cnt: ' + str(adu_read[10:12]))

    #connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP_ADDR, PORT_NO))

    #send packet: read data from registers
    sock.send(adu_read)

    time.sleep(0.05)
    #timeout time set to 3.0 sec
    sock.settimeout(3.0)

    #get values from server
    buffer = sock.recv(BUFSIZE)
    print(buffer)

    sock.close()

    print('transactionID: \t' + str(struct.unpack('>H', buffer[0:2])[0]))
    print('protocolID: \t' + str(struct.unpack('>H', buffer[2:4])[0]))
    print('length: \t' + str(struct.unpack('>H', buffer[4:6])[0]))
    print('unitID: \t' + str(struct.unpack('>B', buffer[6:7])[0]))
    print('Fcode: \t' + str(struct.unpack('>B', buffer[7:8])[0]))
    cnt = struct.unpack('>B', buffer[8:9])[0]
    print('cnt: \t' + str(cnt))
    for i in range(0, cnt, 2):
        print('data: \t' + str(struct.unpack('>H', buffer[i + 9: i + 11])[0]))

"""
-- write to single register in server
--
-- input
--    int unitID: unitID(1byte) 
--    int addr: register's address to write(2byte) 
--    int data: data to be written in register(2byte)
-- output
--    print sent packet
--    print recieved packet
-- prerequisite
--    addr should be givin such as 40001(not 0)
"""
def write_regi(unitID, addr, data):
    #1 ~ 9999 : discrate output coils
    #40001 ~ 49999 : analog output holding registers
    #addr 0 = 0x40001
    if(addr > 10000):
        addr = int(addr % 10000) - 1
    transID = 0
    protocolID = 0
    length = 6       #  len(unit) + len(fcode) + len(addr)  + len(cnt) = 1 + 1 + 2 + 2 = 6 byte
    
    write_fcode = 6  #write to single register  

    #transctionID(2byte) ProtocolID(2byte) length(2byte) unitID(1byte) Fcode(1byte) addr(2bytpe) data(2byte)
    adu_write = struct.pack('>HHHBBHH', transID, protocolID, length, unitID, write_fcode, addr, data)
    print(adu_write)   

    #connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP_ADDR, PORT_NO))

    #send packet:write data to a register
    sock.send(adu_write)

    time.sleep(0.05)
    #timeout time set
    sock.settimeout(3.0)

    sock.close()

if(__name__ == "__main__"):
    hostname = socket.gethostname()
    IP_ADDR = socket.gethostbyname(hostname)
    PORT_NO = 502
    BUFSIZE = 4096

    # write 2020 to a register whose address is 40001
    write_regi(1, 40001, 2020)
    write_regi(1, 40002, 2021)
    write_regi(1, 40003, 2022)

    # read 2 registers starting from 40001
    read_regi(1, 40001, 3)


    


