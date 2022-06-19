"""

Scans possible address range for holding registers, input registers, discrete inputs and coils.
  
Prints 1 if addressable as that type, 0 if not.

Getting through the entire address range could take a few days.

"""

# https://criticallabs.zendesk.com/hc/en-us/articles/360003474273-Modbus-Registers-what-they-mean-and-how-to-interpret-them
# https://www.simplymodbus.ca/FAQ.htm#Map

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.exceptions import ModbusIOException
from pymodbus.pdu import ExceptionResponse

start_address = 0
stop_address = 9999
SIZE = 1
UNIT=1

client = ModbusTcpClient(host="192.168.1.205", port="8899")
print(f"connection status: {client.connect()}")

vals = {}

class Register:

    def __init__(self, new_register):
        self.register = new_register
        self.type_holding_register = None
        self.type_input_register = None
        self.type_input_contact = None
        self.type_status = None


def check_response(response):
    if isinstance(response, ModbusIOException):
        return None
    elif isinstance(response,ExceptionResponse):
        return 0

    return 1


def check_values(vals, start_address, stop_address, size):
    data_address = start_address

    while data_address <= stop_address:

        if data_address not in vals:
            vals[data_address] = Register(data_address)

        register = vals[data_address]
        
        if not register.type_holding_register:
            response = client.read_holding_registers(data_address, size, unit=UNIT)
            check = check_response(response)
            if check is None:
                continue
            register.type_holding_register = check

        if not register.type_input_register:
            response = client.read_input_registers(data_address, size, unit=UNIT)
            check = check_response(response)
            if check is None:
                continue
            register.type_input_register = check

        if not register.type_input_contact:
            response = client.read_discrete_inputs(data_address, size, unit=UNIT)
            check = check_response(response)
            if check is None:
                continue
            register.type_input_contact = check

        if not register.type_status :
            response = client.read_coils(data_address, size, unit=UNIT)
            check = check_response(response)
            if check is None:
                continue
            register.type_status  = check

        print(f"{data_address}\t{register.type_holding_register}\t{register.type_input_register}\t{register.type_input_contact}\t{register.type_status}")
        data_address += size


print(f"\n\nAddr\tHoldReg\tInReg\tInDisc\tCoils\n")
check_values(vals, start_address, stop_address, SIZE)
