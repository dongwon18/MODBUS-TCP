"""
-- Copyright 2021. Dongwon Kim All rights reserved.
--
-- File name : decoding.py
-- 
-- Written by Dongwon Kim
--
-- Modbus TCP communication(header file)
--    Decode data from Modbus server
--        server: Gastron GTD-5000, Honeywell Midas Gas Detector
--
-- Modificatoin history
--    written by Dongwon Kim on June 18, 2021
--
-- Encoding: UTF-8
--
"""

"""
Get Status of Gas detector
precedence
    1. Fault Active
    2. Alarm2
    3. Alarm1
    4. Monitoring Status
input:
    str status: bit string from the detector, xxxxxxxxxxxxxxxx(len: 16)
    int detector: Gastron(0), Honeywell(1) 

output:
    result: string of status
"""
def decode_status(status, detector):
    #Gastron
    if(detector == 0):
        monitoring = status[0:4]
        if(monitoring == '0000'):
            result = "Warm up"
        elif(monitoring == '0001'):
            result = "Measureing"
        elif(monitoring == '0010'):
            result = "Inspection"
        elif(monitoring == '0111'):
            result = "20mA Correction"
        elif(monitoring == '1000'):
            result = "Flow Correction"
        else:
            result = "[Error] No such mode"
        
        if(status[6] == '1'):
            result = "Alarm 1"
        if(status[7] == '1'):
            alarm2 = "Alarm 2"
        if(status[4] == '1'):
            result = "Fault Active"

    #Honeywell
    elif(detector == 1):
        monitoring = status[0:4]
        if(monitoring == '0000'):
            result = "Warm up"
        elif(monitoring == '0001'):
            result = "Measureing"
        elif(monitoring == '0010'):
            result = "Inspection"
        elif(monitoring == '0111'):
            result = "20mA Correction"
        elif(monitoring == '1000'):
            result = "Flow Correction"
        else:
            result = "[Error] No such mode"
        
        if(status[6] == '1'):
            result = "Alarm 1"
        if(status[7] == '1'):
            alarm2 = "Alarm 2"
        if(status[4:6] == '00'):
            result = "No fault"
        elif(status[4:6] == '01'):
            result = "Maintenance fault active"
        elif(status[4:6] == '10'):
            result = "Instrument fault active"
        else:
            result = "[Error] No such fault status " + str(status[4:6])
    else:
        result = "[Error] No such detector " + str(detector)

    return result

"""
Get gas_value
input:
    str value: bit string from the detector, xxxxxxxxxxxxxxxx...xx(len: 32)
    int detector: Gastron(0), Honeywell(1) 
    int dp: decimal point indecator
output:
    return str gas value including decimal point(Gastron, Honeywell)
           str error message(other detector)
"""
def decode_gas_value(value, detector, dp):
    if(detector == 0 or detector == 1):
        value = int(value, 2)
        value = str(value)
        #if dp = 2, 12345 -> 123.45
        gas_value = value[0:len(value) - dp] + '.' + value[len(value) - dp:]
    else:
        gas_value = "[Error] No such data for the detector" + str(detector)
    return gas_value


"""
Get Error code
input:
    str error_code: bit string from the detector, 0bxxxxxxxxxxxxxxxx
    int detector: Gastron(0), Honeywell(1) 
    
output:
    return  error code value in string(Gastron)
            error message in string(other detector)
"""
def decode_error_code(error_code, detector):
    if(detector == 0):
        error_code = int(error_code)
        return str(error_code)
    else:
        error_string = "[Error] No such data for the detector" + str(detector)
        return error_string


"""
Get unit
input:
    str error_code: bit string from the detector, 0bxxxxxxxxxxxxxxxx
    int detector: Gastron(0), Honeywell(1) 
output:
    return str of unit for proper detector no.
           error message in str(other detector)
"""
def decode_units(unit, detector):
    if(detector == 0):
        values = unit[8:12]
        if(values == '0001'):
            return "PPM"
        elif(values == '0010'):
            return "PPB"
        elif(values == '0100'):
            return "% Volume"
        elif(values == '1000'):
            return "% LEL"
        else: 
            return "[Error] No such unit code " + values

    elif(detector == 1):
        values = unit[8:16]
        if(values == '00000001'):
            return "PPM"
        elif(values == '00000010'):
            return "PPB"
        elif(values == '00000100'):
            return "% Volume"
        elif(values == '00001000'):
            return "% LEL"
        elif(values == '00010000'):
            return "mA"
        else:
            return "[Error] No such unit code " + values   
        

"""
Get decimal point
input:
    str unit: bit string from the detector, 0bxxxxxxxxxxxxxxxx
    int detector: Gastron(0), Honeywell(1) 
output:
    return int result: no. of decimal point(Gastron, Honeywell)
           str error message (other detector)
"""
def decode_decimal_point(unit, detector):
    decimal = unit[0:3]
    if(detector == 0 or detector == 1):
        if(decimal == '000'):
            return 0
        elif(decimal == '001'):
            return 1
        elif(decimal == '010'):
            return 2
        elif(decimal == '011'):
            return 3
    else:
        return "[Error] No such detector " + str(detector)


"""
Get alarm's limit value
input:
    str alarm_limit: bit string from the detector, 0bxxxxxxxxxxxxxxxx...xx(max: 32)
    int detector: Gastron(0), Honeywell(1) 
    int dp: decimal point indecator
output:
    return str alarm's limit value including decimal point(Gastron, Honeywell)
           str error message(other detector)
"""
def decode_alarm_limit(alarm_limit, detector, dp):
    if(detector == 0 or detector == 1):
        value = int(alarm_limit, 2)
        value = str(value)
        return value[0:len(value) - dp] + '.' + value[len(value) - dp:]
    else:
        return "[Error] No such detector " + str(detector)

"""
Get gas information
input:
    str gas_info: bit string from the detector, 0bxxxxxxxxxxxxxxxx
    int detector: Gastron(0), Honeywell(1)

output:
    return str gasID, catridgeID(Honeywell)
           str error message(other detector)
"""
def decode_gas_info(gas_info, detector):
    if(detector == 1):
        gas_id = gas_info[0:8]
        gas_id = int(gas_id, 2)
        gas_id = str(gas_id)
        cat_id = gas_info[8:16]
        cat_id = int(cat_id, 2)
        cat_id = str(cat_id)
    else:
        gas_id = "[Error] No gas ID for detector " + str(detector)
        cat_id = "[Error] No Cartridge ID for detector " + str(detector)

    return gas_id, cat_id


# In[5]:


#get_ipython().system('jupyter nbconvert --to python decoding.ipynb')
