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
num_values_to_read = 500


client = ModbusTcpClient(host="192.168.1.205", port="8899")
print(f"connection status: {client.connect()}")

vals = {}

def save_value(timestamp, address, bits, file):
    """Save value to a file."""
    print(f"{timestamp}\t{address}\t{bits}", file=file)

def get_data(address, size):
    """Get data from unit."""
    try:
        response = client.read_holding_registers(address, size, slave=UNIT)
    except ConnectionException:
        client.connect()
        return get_data(address, size)

    if response.isError():
        return get_data(address, size)

    return response

def check_block(start_address, size, file):
    """Check a block of values."""
    print(f"check_block start: {start_address}, size: {size}")
    response = get_data(start_address, size)
    current_datetime = datetime.now().strftime('%x %X')
 
    i = 0
    for bits in response.registers:
        save_value(current_datetime, start_address+i, bits, file)
        i +=1

with open("changes.txt", "a") as f:
    for x in range(1,num_values_to_read):
        print(f"check values try {x}")
        check_block(0, 100, f)
        check_block(100, 100, f)        
        check_block(200, 100, f)        
        check_block(300, 100, f)                
        check_block(400, 100, f)        
        check_block(500, 100, f)        
        check_block(600, 100, f)        
        check_block(700, 100, f)        
        check_block(800, 8, f)        

