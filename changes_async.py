"""Read registers and look for changing values to help determine what each address holds."""

import logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)-8s %(name)s:  %(message)s",
    filename="test.log",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
)

_LOGGER = logging.getLogger()
_LOGGER.info("starting script")
import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ConnectionException

SIZE = 1
UNIT=1

_LOGGER.info("set up client")
client = AsyncModbusTcpClient(host="192.168.1.205", port="8899", timeout=10, strict=False)
_LOGGER.info("set up client done")

async def connect():
    _LOGGER.info(f"try to connect")
    await client.connect()
    _LOGGER.info(f"client connected: {client.connected}")
    

async def get_value(address):
    try:
        #async with async_timeout.timeout(30):
        _LOGGER.info(f"client connected: {client.connected}")
        response = await client.read_holding_registers(address, SIZE, slave=UNIT)
        _LOGGER.info("response")
    except ConnectionException:
        print("not connected")
        return False

    if response.isError():
        print("error")
        return False        

    bits = response.registers[0]
    print(bits)
    return True

"""
asyncio.run(connect(), debug=True)
print("try getting value")
#asyncio.run(get_value(3))
asyncio.run(get_value(4), debug=True)
asyncio.run(get_value(5))
print("still waiting?")
"""


async def main():
    await asyncio.sleep(1)
    await connect()
    await get_value(4)

asyncio.run(main())