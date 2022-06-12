from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException

index = 0x00
size = 1

client = ModbusTcpClient(host="192.168.1.205", port="8899")

print(f"connection status: {client.connect()}")

# address 3 to 7 appears to be Inverter Serial Number.  Nothing else is obvious.

print("Read holding registers")
while index < 0xff:
    response = client.read_holding_registers(index, size, unit=1)
    if not isinstance(response, ModbusIOException):
        bits = response.registers[0]
        unichar = chr(bits)
        byte1 = bits & 0xff
        byte2 = bits >> 8 
        char1 = chr(byte1)
        char2 = chr(byte2)

        print(f"{index}\t{bits}\t{unichar}\t{char2}\t{char1}")

    index += size

#decoder = BinaryPayloadDecoder.fromRegisters(response.registers)
#while index < size:
#    print( "{index}]\t{decoder}")

