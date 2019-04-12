# import logging
# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

import pymodbus
from pymodbus.client.sync import ModbusSerialClient as modclient
from pymodbus.register_read_message import ReadInputRegistersRequest
from pymodbus.register_read_message import ReadHoldingRegistersRequest


# client1 = modclient(method='rtu', port='/dev/ttyUSB0', stopbits=1, bytesize=8, baudrate=19200)
client1 = modclient(method='rtu', port='com9', stopbits=2, bytesize=8, baudrate=9600)

conn = client1.connect()
print(conn)



# valuehr = client1.read_holding_registers(100,2,unit=0x01)
valuehr = client1.read_holding_registers(64,1,unit=0x01)
print type(valuehr)
print valuehr.registers


client1.close()