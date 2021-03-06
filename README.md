# modbus_mapper
Python scripts to attempt to map out an unknown MODBUS registry map using a TCP based "logger" with the goal of reading device data.

The ultimate goal is to integrate the device into Home Assistant.

While this focuses on solar related equipment for Home Assistant, the general plan and mapping scripts could apply to any unknown MODBUS device.

Assumptions:
- You have a functioning logger device already connected to your network, and your logger uses port 8899.
- You followed the directions for the [Solarman integration](https://github.com/StephanJoubert/home_assistant_solarman/) and realized your device is unknown and needs a custom parameter file.
- You asked your solar device manufacturer for the MODBUS registry mapping

## Overall strategy
The basic plan is to piece together what little information you have to try to build a custom parameter file.  Like a jigsaw puzzle, we will slowly put the pieces together.

- Gain access to the device
- Map out "addressable" registers
- See what registers hold no data and ignore them
- See what registers hold static data (like your serial #)
- See what registers hold changing data
- Make educated guesses about what registers hold what data

## Find the logger device


Use `nmap` or other tools to find the logger

```cmd
nmap -p 8899 192.168.1.1/24
```
Look for IP addresses that say `STATE open`.  Note the IP address and MAC address.

Try http://<IP_address> to see if the device has a web interface that may provide info.

The LSE-3 stick logger has a web interface and provides a little information that may be useful, including the logger serial number.  The serial number is likely on a sticker on the stick logger.

## Setup this script

Clone the repository and then run
```cmd
pip install -r requirements.txt
```

## The hard part - Trial and Error
Now comes the hard part, using trial and error to figure out what the registers are.

First use `scan.py` to scan the device and see what registers respond as what type.  Second user `changes.py` to read in values.

### scan.py

Near the top of the `scan.py` file, change the `IP_ADDRESS` to the address of your device.  Now run the script:

```cmd
python scan.py
```

It could take a very long time (hours) to scan all of the possible addresses.  If you have information about the address range of your device, change the `start_address` or `stop_address` variables at the top of the script to save some time.

Now you know what registers are responding, and as what type.  

### changes.py

This script creates a text file that simply lists each address and what the value is when it's read.  It uses a date/time format compatible with Microsoft Excel, so it can be easily pasted into a spreadsheet for examination.  

Change the `start_address` or `stop_address` variables at the top of the script to match what you learned from `scan.py`

The script assumes your device uses "holding registers".  If your device uses something different, the script will have to be adjusted.

The script creates a file called `changes.txt`.  If the file already exists, data will be appended to the end of the file.  This is useful so you can run the script many times over the course of a few days, because (given the name) you are looking for changes.

Examples of types of changes you will see:

- Daily counter/total: slowly adds up over the day, but resets to zero at midnight.  Could be for "daily energy produced" or some similar parameter.
- Weekly/Monthly/Other total: slowly adds up, but resets at some interval greater than a single day.  Could be for weekly/monthly/annual/total energy produced.
- Increasing with sun: some parameter that clearly increases in value when the sun is up, likely related to solar production.
- Increasing with usage: some parameter associated with time of high usage, which could be at night.
- Increasing/decreasing with a limit: something like a battery, that goes between zero and one hundred percent

## Contributing back to the community
If you get it working, contribute back to the larger community by sharing your parameters file via a Pull Request to the Solarman integration.

If you improve on these scripts, or have better ideas on how to find the MODBUS parameters, pull requests to this repo are very welcome.

## Related work or info
- Home Assistant HACS integration for [Solarman](https://github.com/StephanJoubert/home_assistant_solarman/)

