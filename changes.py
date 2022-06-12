from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse

index = 0
num_to_try = 898
SIZE = 1
UNIT=1

client = ModbusTcpClient(host="192.168.1.205", port="8899")
print(f"connection status: {client.connect()}")

vals = {}

class Value:

    def __init__(self, new_register, new_value):
        self.register = new_register
        self.value = 0
        self.byte1 = 0
        self.byte2 = 0
        self.changed = 0
        self.num_changes = 0
        self.zero = 1
        self.char1 = ""
        self.char2 = ""
        self._set(new_value)

    def update(self, new_value):
        if self.value != new_value:
            self.changed = 1
            self.num_changes += 1
            self._set(new_value)

    def _set(self, new_value):
        self.value = new_value
        self.byte1 = new_value & 0xff
        self.byte2 = new_value >> 8
        self.char1 = chr(self.byte1)
        self.char2 = chr(self.byte2)
        if new_value != 0:
            self.zero = 0


def check_values(vals, index, tries):
    while index < tries:
        response = client.read_holding_registers(index, SIZE, unit=UNIT)
        while response.isError():
            response = client.read_holding_registers(index, SIZE, unit=UNIT)

        bits = response.registers[0]
        print(f"index {index}: {bits}")

        if index not in vals:
            vals[index] = Value(index, bits)
        else:
            vals[index].update(bits)

        index += SIZE



for x in range(1,5):
    print(f"check values try {x}")
    check_values(vals, index, num_to_try)


print(f"index\t16bit\tchanged\tzero\tbyte2\tbyte1\n")
for value in vals.values():
    print(f"{value.register}\t{value.value}\t{value.changed}\t{value.zero}\t{value.byte2}\t{value.byte1}")
