from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder

#    template = ['address', 'size', 'function', 'name', 'description']
#    raw_mapping = csv_mapping_parser('input.csv', template)
#    mapping = mapping_decoder(raw_mapping)

index, size = 1, 100
client = ModbusTcpClient(host='192.168.1.205', port='8899')
response = client.read_holding_registers(index, size)
decoder = BinaryPayloadDecoder.fromRegisters(response.registers)
while index < size:
    print( "[{}]\t{}".format(i, mapping[i]['type'](decoder)))
    index += mapping[i]['size']
