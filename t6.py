from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse

index = 0
num_to_try = index + 1000
size = 1
unit=1

client = ModbusTcpClient(host="192.168.1.205", port="8899")

print(f"connection status: {client.connect()}")

# address 3 to 7 appears to be Inverter Serial Number.  Nothing else is obvious.

print("Read input registers")
while index < num_to_try:
    #response = client.read_input_registers(index, size, unit=unit)
    response = client.read_holding_registers(index, size, unit=unit)
    if isinstance(response, ModbusIOException):
        print(f"{index}\tModbusIOException: {response}")
    elif isinstance(response,ExceptionResponse):
        print(f"{index}\tExceptionResponse: {response}")
    else:
        bits = response.registers[0]
        unichar = chr(bits)
        byte1 = bits & 0xff
        byte2 = bits >> 8 
        char1 = chr(byte1)
        char2 = chr(byte2)

        print(f"{index}\t{int(bits)}\t{float(bits)}\t{char2}{char1}")


    index += size

#decoder = BinaryPayloadDecoder.fromRegisters(response.registers)
#while index < size:
#    print( "{index}]\t{decoder}")

