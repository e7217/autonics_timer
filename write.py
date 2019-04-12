# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

import pymodbus
from pymodbus.client.sync import ModbusSerialClient as modclient
from pymodbus.register_read_message import ReadInputRegistersRequest
from pymodbus.register_read_message import ReadHoldingRegistersRequest

# modbus : ('coil' or 'holding')
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

    print type(valuecheck)

    client1.close()

def readFromCounter(modbus, address):

    # client1 = modclient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, baudrate=19200)
    conn = client1.connect()
    # print('connection status : ', conn)

    if modbus == 'coil' :
        valuecheck = client1.read_coils(address, 1, unit=0x01)
        print valuecheck.bits[0]
    elif modbus == 'holding' :
        valuecheck = client1.read_holding_registers(address, 1, unit=0x01)
        # print valuecheck.registers

    # print type(valuecheck)

    client1.close()

    return valuecheck

client1 = modclient(method='rtu', port='com9', stopbits=2, bytesize=8, baudrate=9600)

# writeToCounter('coil', 0, 1)

list = [0, 2, 4, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 64, 65, 100, 102, 103, 104, 105, 106, 107, 108, 109, 150, 151, 152, 153, 154, 155]

for i in list:
    print i, ':', readFromCounter('holding', i).registers
