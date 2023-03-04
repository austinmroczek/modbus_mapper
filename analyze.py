"""

Analyze data saved by changes.py

"""

### ASSUMPTION:  data is in time order in input file

import pandas as pd
from address_analyzer import AddressAnalyzer16


#read in data from file
# parse_dates=[0] reads the first column as a datetime
data = pd.read_csv("changes.txt", delimiter='\t', names = ['timestamp', 'address', 'value'], parse_dates=[0])

# find start and stop point
addresses = data['address']
start_address = addresses.min()
stop_address = addresses.max()
print(f"Start address: {start_address}")
print(f"Stop address: {stop_address}")


# add some new columns based on existing data

# datetime
data["year"] = data["timestamp"].dt.year
data["month"] = data["timestamp"].dt.month
data["day_of_year"] = data["timestamp"].dt.day_of_year
data["day_of_week"] = data["timestamp"].dt.day_of_week
data["day"] = data["timestamp"].dt.day
data["hour"] = data["timestamp"].dt.hour
data["minute"] = data["timestamp"].dt.minute

# 16 bit signed value
data["signed_value"] = data.apply(lambda row: row.value if row.value < 2^15 else 2^15 - row.value, axis=1)




zeros = []
fixed = []
increasing = []
decreasing = []
results = []

for address in range(start_address, stop_address + 1):
    d = data[data["address"] == address]
    result = AddressAnalyzer16(address, d)

    results.append(result)

for result in results:
    result.print_results()




