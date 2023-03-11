"""Read registers and look for changing values to help determine what each address holds."""

from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException, ConnectionException
from pymodbus.pdu import ExceptionResponse

from common import Value

start_address = 0
stop_address = 808
SIZE = 1
UNIT=1

client = ModbusTcpClient(host="192.168.1.205", port="8899")
print(f"connection status: {client.connect()}")

vals = {}

def check_values(vals, address, size=1):
    try:
        response = client.read_holding_registers(address, size, slave=UNIT)
    except ConnectionException:
        client.connect()
        return check_values(vals, address, size=size)

    if response.isError():
        return check_values(vals, address, size=size)

    address += size

num_to_test = 100
start_time = datetime.now()
for x in range(0,num_to_test):
#    print(f"check values try {x}")
    check_values(vals, 0, size=1)
end_time = datetime.now()
time_difference = end_time - start_time
rate_per_second = time_difference.total_seconds() / 100
print(f"seconds per value (fetching 1 at a time): {rate_per_second}")

num_to_test = 10
start_time = datetime.now()
for x in range(0,num_to_test):
    #print(f"check values try {x}")
    check_values(vals, 0, size=10)
end_time = datetime.now()
time_difference = end_time - start_time
rate_per_second = time_difference.total_seconds() / 100
print(f"seconds per value (fetching 10 at a time): {rate_per_second}")

num_to_test = 100
start_time = datetime.now()
#print(f"check values try {x}")
check_values(vals, 0, size=100)
end_time = datetime.now()
time_difference = end_time - start_time
rate_per_second = time_difference.total_seconds() / 100
print(f"seconds per value (fetching 100 at a time): {rate_per_second}")

# NOTE:  testing shows grabbing more at a time is much faster.