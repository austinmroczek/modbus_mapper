from modbus_mapper import csv_mapping_parser
from modbus_mapper import mapping_decoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryModbusDecoder

template = ["address", "size", "function", "name", "description"]
raw_mapping = csv_mapping_parser("input.csv", template)
mapping = mapping_decoder(raw_mapping)

index, size = 1, 100
client = ModbusTcpClient("localhost")
response = client.read_holding_registers(index, size)
decoder = BinaryModbusDecoder.fromRegisters(response.registers)
while index < size:
    print( "[{}]\t{}".format(i, mapping[i]["type"](decoder)))
    index += mapping[i]["size"]
