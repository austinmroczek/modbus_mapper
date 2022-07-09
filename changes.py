"""Read registers and look for changing values to help determine what each address holds."""

from datetime import datetime
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException, ConnectionException
from pymodbus.pdu import ExceptionResponse

from .common import Value

start_address = 23
stop_address = 808
SIZE = 1
UNIT=1

client = ModbusTcpClient(host="192.168.1.205", port="8899")
print(f"connection status: {client.connect()}")

vals = {}

def check_values(vals, address, tries, f):
    while address < tries:

        try:
            response = client.read_holding_registers(address, SIZE, unit=UNIT)
        except ConnectionException:
            client.connect()
            return check_values(vals, address, tries, f)

        if response.isError():
            return check_values(vals, address, tries, f)

        bits = response.registers[0]
        current_datetime = datetime.now().strftime('%x %X')

        if address not in vals:
            vals[address] = Value(address, bits)
            # print initial value
            print(f"{current_datetime}\t{address}\t{bits}", file=f)
        else:
            vals[address].update(bits)
            
        if vals[address].changed:
            # print any changed values
            print(f"{current_datetime}\t{address}\t{bits}", file=f)

        address += SIZE

with open("changes.txt", "a") as f:
    for x in range(1,500):
        print(f"check values try {x}")
        check_values(vals, start_address, stop_address, f)


print(f"address\t16bit\tchanged\tzero\tbyte2\tbyte1\n")
for value in vals.values():
    print(f"{value.register}\t{value.value}\t{value.changed}\t{value.zero}\t{value.byte2}\t{value.byte1}")
