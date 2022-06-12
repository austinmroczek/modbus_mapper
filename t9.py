from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse

index = 8
num_to_try = index + 1000
size = 2
unit=1

client = ModbusTcpClient(host="192.168.1.205", port="8899")
print(f"connection status: {client.connect()}")

# address 3 to 7 appears to be Inverter Serial Number.  Nothing else is obvious.
response = client.read_holding_registers(3, 4, unit=unit)

while response.isError():
    print(f"Error:\n{response}")
    response = client.read_holding_registers(3, 4, unit=unit)

decoder = BinaryPayloadDecoder.fromRegisters(response.registers)
serial_number = decoder.decode_string(8).decode()
print(f"Serial number: {serial_number}")




# read other registers

print("Read input registers")
while index < num_to_try:
    response = client.read_holding_registers(index, size, unit=unit)
    while response.isError():
        response = client.read_holding_registers(index, size, unit=unit)

    decoder = BinaryPayloadDecoder.fromRegisters(response.registers)

    try:
        n_str = decoder.decode_string(2).decode()
    except UnicodeDecodeError:
        n_str = ""

    decoder.reset()
    n_int32 = decoder.decode_32bit_int()
    decoder.reset()
    n_int32u = decoder.decode_32bit_uint()
    decoder.reset()
    n_float32 = decoder.decode_32bit_float()
    decoder.reset()
    print(f"{index}\t{n_int32}\t{n_int32u}\t{n_float32}")


    index += size


