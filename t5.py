from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder

from pymodbus.mei_message import ReadDeviceInformationRequest
from pymodbus.device import ModbusDeviceIdentification

index = 0x00
size = 4
UNIT=0x1

client = ModbusTcpClient(host="192.168.1.205", port="8899")

print(f"connection status: {client.connect()}")

print(f"Read device information")

information = {}
rr = None

while not rr or rr.more_follows:
    next_object_id = rr.next_object_id if rr else 0
    #rq = ReadDeviceInformationRequest(
    #    read_code=0x03, unit=UNIT, object_id=next_object_id
    #)
    rq = ReadDeviceInformationRequest(read_code=0x01,unit=UNIT,object_id=next_object_id)
    print(f"\tRequest: {rq}")
    rr = client.execute(rq)
    print(f"\tRequestResponse: {rr}")
    information.update(rr.information)

print(f"{information}")

print("Read registers")
while index < 0xff:
    response = client.read_holding_registers(index, size, unit=1)
    print(f"{index}: {response.registers}")
    index += 4

#decoder = BinaryPayloadDecoder.fromRegisters(response.registers)
#while index < size:
#    print( "{index}]\t{decoder}")

