import pymodbus
from pymodbus.client.sync import ModbusSerialClient as modclient
from pymodbus.register_read_message import ReadInputRegistersRequest
from pymodbus.register_read_message import ReadHoldingRegistersRequest

from time import sleep
import sys
import io
import pymssql
import time
import datetime

# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

# ------------------------ configuration using dict -------------------------------------

def confEnv(filename):
    ## (190401) check for ':' exist.
    def isport(dict_):
        if dict_['port'] != '':
            dict_['server'] = dict_['server'] + ':' + dict_['port']
        return dict_

    dict = {'port': ''}
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            comp = line.split('=')
            for i in range(len(comp)):
                comp[i] = comp[i].strip()
            if (comp[0] == "server") and (comp[1].find(":") > 0):
                dict[comp[0]], dict['port'] = (comp[1].split(':'))[0], (comp[1].split(':'))[1]
            else:
                dict[comp[0]] = comp[1]
    return isport(dict)

# --------------------------------------------------------------------------------------

# modbus : ('coil' / 'holding' / 'analog')
def writeToCounter(modbus, address, value):

    # client1 = modclient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, baudrate=19200)
    # client1 = modclient(method='rtu', port='com9', stopbits=2, bytesize=8, baudrate=9600)

    conn = client1.connect()
    print('connection status : ', conn)

    if modbus == 'coil' :
        client1.write_coil(address, value, unit=0x01)
        valuecheck = client1.read_coils(address, 1, unit=0x01)
        print valuecheck.bits[0]
    elif modbus == 'holding' :
        client1.write_register(address, value, unit=0x01)
        valuecheck = client1.read_holding_registers(address, 1, unit=0x01)
        print valuecheck.registers

    # print type(valuecheck)
    client1.close()

def readFromCounter(modbus, address):

    # client1 = modclient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, baudrate=19200)
    conn = client1.connect()
    # print('connection status : ', conn)

    if modbus == 'coil' :
        valuecheck = client1.read_coils(address, 1, unit=0x01)
        print 'value : ', valuecheck.bits[0]
    elif modbus == 'holding' :
        valuecheck = client1.read_holding_registers(address, 1, unit=0x01)
        print 'value : ', valuecheck.registers
    elif modbus == 'analog':
        valuecheck = client1.read_input_registers(address, 1, unit=0x01)
        print 'value : ', valuecheck.registers

    # print type(valuecheck)

    client1.close()

    return valuecheck

def do(value):
    try:
        conn = pymssql.connect(envList['server'], envList['user'], envList['password'], envList['database'], timeout=3)
        time.sleep(0.01)
        print 'db_step_1'
        cursor = conn.cursor()
        time.sleep(0.01)
        print 'db_step_2'
        cursor.callproc('usp_xngat11t_i02', [None, mchcd, 'D', value])
        time.sleep(0.01)
        cursor.callproc('usp_xnwrk_u', [mchcd])
        time.sleep(0.01)
        # works.
        print 'db_step_3-1'
        cursor.callproc('usp_xngat11t_i02', [None, mchcd, 'S', 0])
        time.sleep(0.01)
        print 'db_step_3-2'
        # g1.reset_()
        writeToCounter('coil', resetAddress, forResetValue)
        conn.commit()
        time.sleep(0.01)
        print 'db_step_4'
        conn.close()
        time.sleep(0.01)
        print 'db_step_5 connection closed'

    except:
        print 'retry'
        do(value)

def input(value):
    try:
        conn = pymssql.connect(envList['server'], envList['user'], envList['password'], envList['database'], timeout = 3)
        time.sleep(0.01)
        print 'db_step_1'
        cursor = conn.cursor()
        time.sleep(0.01)
        print 'db_step_2'
        # works.
        cursor.callproc('usp_xngat11t_i02', [None, mchcd, 'D', value])
        time.sleep(0.01)
        print 'db_step_3'
        conn.commit()
        time.sleep(0.01)
        print 'db_step_4'
        conn.close()
        time.sleep(0.01)
        print 'db_step_5 connection closed'

    except :
        print 'retry'
        input()
# ------------------------ setting environments ----------------------------------------

# Configure Count and Reset Protocol
client1 = modclient(method='rtu', port='com9', stopbits=2, bytesize=8, baudrate=9600)
countValueAddress = 1003 # modbus : 'analog'
resetAddress = 0 # modbus : 'coil'
forResetValue = 1

# Configuration from an environments file.
fc_path= './env/connect_env.txt'
envList = confEnv(fc_path)
server = envList['server']
user = envList['user']
password = envList['password']
database = envList['database']
mchcd = envList['machine']

# resetProtocol : 01 05 00 00 FF 00 8C 3A'
# --------------------------------------------------------------------------------------

# protocol for reset
# writeToCounter('coil', resetAddress, forResetValue)
# readFromCounter('analog', countValueAddress)
# readFromCounter('analog', 1006)

#todo: inputdata

while (True) :
    countValue = readFromCounter('analog', countValueAddress).registers
    time.sleep(10)

    # todo: reset countValue at 8 a.m
    resettime = datetime.datetime.now().time()
    if resettime > datetime.time(07,54) and resettime < datetime.time(07,55):
        do(countValue)
    else:
        input(countValue)



#todo: check response.
