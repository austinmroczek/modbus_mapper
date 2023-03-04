"""Analyzer class."""

import string
from scipy.fft import rfft
from datetime import datetime


MIN_UNIQUE_PERCENT = 5
MIN_UNIQUE_HERTZ = 5


class AddressAnalyzer16:
    """Analyzes a 16-bit address."""

    def __init__(self, address, data):
        """Initiate with an address."""
        self._address = address
        self._data = data
        self._changes = None
        self._zero = None
        self._increasing = None
        self._decreasing = None
        self._ascii = None

        self._num_unique = None

        self._unsigned_max = None
        self._unsigned_min = None
        self._unsigned_mean = None
        self._unsigned_median = None

        self._signed_max = None
        self._signed_min = None
        self._signed_mean = None
        self._signed_median = None

        self._c_year = None
        self._c_month = None
        self._c_day_of_month = None
        self._c_day_of_week = None
        self._c_day_of_year = None
        self._c_hour = None
        self._c_minute = None

        self._analyze()

    def __str__(self):
        """Print."""
        text = f"Address: {self.address}"
        if self.is_fixed:
            text = text + f"\tFixed Value: {self.value}"

        else:
            if self.is_increasing:
                text = text + f"\tIncreasing from {self.unsigned_min} to {self.unsigned_max}"

            if self.is_decreasing:
                text = text + f"\tDecreasing from {self.unsigned_max} to {self.unsigned_min}"

            text = text + f"\tMean: {self.unsigned_mean}"
            text = text + f"\tMedian: {self.unsigned_median}"

        return text



    def is_changing(self):
        """Return true if values are changing over time."""
        return self._changes

    def is_fixed(self):
        """Return true if value never changes."""
        return not self._changes

    def is_zero(self):
        """Return true if value is always zero."""
        return self._zero

    def is_increasing(self):
        """Return true if values only increase over time."""
        return self._increasing

    def is_decreasing(self):
        """Return true if values only decrease over time."""
        return self._decreasing

    def is_ascii(self):
        """Return true if always contains valid ASCII characters."""

        # TODO
        """
        self.byte1 = new_value & 0xff
        self.byte2 = new_value >> 8
        self.char1 = chr(self.byte1)
        self.char2 = chr(self.byte2)

        if self.char1 in string.printable and self.char2 in string.printable:
            self.is_ascii = True
        """

        return self._ascii

    def _analyze(self):
        """Analyze all data."""

        self._num_unique = self._data["value"].nunique()
        self._check_changing()
        self._check_zero()

        if self.is_zero():
            return

        # what about fixed ?

        if self.is_changing():
            self._check_increasing_decreasing()

        self._unsigned_max = self._data["value"].max()
        self._unsigned_min = self._data["value"].min()
        self._unsigned_mean = round(self._data["value"].mean(),1)
        self._unsigned_median = self._data["value"].median()

        self._signed_max = self._data["signed_value"].max()
        self._signed_min = self._data["signed_value"].min()
        self._signed_mean = round(self._data["signed_value"].mean(),1)
        self._signed_median = self._data["signed_value"].median()

        self._c_year = round(self._data['value'].corr(self._data['year']),2)
        self._c_month = round(self._data['value'].corr(self._data['month']),2)
        self._c_day_of_month = round(self._data['value'].corr(self._data['day']),2)
        self._c_day_of_week = round(self._data['value'].corr(self._data['day_of_week']),2)
        self._c_day_of_year = round(self._data['value'].corr(self._data['day_of_year']),2)
        self._c_hour = round(self._data['value'].corr(self._data['hour']),2)
        self._c_minute = round(self._data['value'].corr(self._data['minute']),2)

    def print_results(self):
        """Print out results."""
        if self.is_zero():
            # don't print zero
            return

        if self.is_fixed():
            #don't print fixed
            return

        print(f"Address {self._address}: min {self._unsigned_min:5d}\tmean {self._unsigned_mean:7.1f}\tmedian {self._unsigned_median:7.1f}\tmax {self._unsigned_max:5d}\tunique: {self._num_unique:5d}")

        if self.is_increasing():
            print(f"\tincreasing")

        if self.is_decreasing():
            print(f"\tdecreasing")

        if self._c_year > .95 and self.is_increasing():
            print(f"\tcorrelates {self._c_year} with year")

        if self._c_month > .95:
            print(f"\tcorrelates with month {self._c_month}")

        if self._c_day_of_month > .95:
            print(f"\tcorrelates with day of month {self._c_day_of_month}")                        

        if self._c_day_of_week > .95:
            print(f"\tcorrelates with day of week {self._c_day_of_week}")                                    

        if self._c_day_of_year > .95:
            print(f"\tcorrelates with day of year {self._c_day_of_year}")     


        # will not get perfect correlation with hour because not generating every hour of the day
        if self._c_hour > .50:
            print(f"\tcorrelates with hour {self._c_hour}")                        

        if self._c_minute > .95:
            print(f"\tcorrelates with minute {self._c_minute}")                        

        # potential Frequency, unsigned most likely
        if self._is_hertz(self._data["value"], self._unsigned_mean, 1):
            print(f"\tpotential 60 Hertz Frequency at 1.0 scale unsigned")
        if self._is_hertz(self._data["value"],self._unsigned_mean, 0.1):
            print(f"\tpotential 60 Hertz Frequency at 0.1 scale unsigned")
        if self._is_hertz(self._data["value"],self._unsigned_mean, 0.01):
            print(f"\tpotential 60 Hertz Frequency at 0.01 scale unsigned")

        #...but try signed just in case
        if self._is_hertz(self._data["signed_value"],self._signed_mean, 1):
            print(f"\tpotential 60 Hertz Frequency at 1.0 scale")
        if self._is_hertz(self._data["signed_value"],self._signed_mean, 0.1):
            print(f"\tpotential 60 Hertz Frequency at 0.1 scale")
        if self._is_hertz(self._data["signed_value"],self._signed_mean, 0.01):
            print(f"\tpotential 60 Hertz Frequency at 0.01 scale")


        # TODO:  just using mean is not correct for things that fluctuate up and down...

        # potential 120 volts
        if self._is_voltage_120(self._unsigned_mean, self._unsigned_max, 1):
            print(f"\tpotential 120 Volts at 1.0 scale")
        if self._is_voltage_120(self._unsigned_mean, self._unsigned_max, 0.1):
            print(f"\tpotential 120 Volts at 0.1 scale")
        if self._is_voltage_120(self._unsigned_mean, self._unsigned_max, 0.01):
            print(f"\tpotential 120 Volts at 0.01 scale")

        if self._is_voltage_240(self._unsigned_mean, self._unsigned_max, 1):
            print(f"\tpotential 240 Volts at 1.0 scale")
        if self._is_voltage_240(self._unsigned_mean, self._unsigned_max, 0.1):
            print(f"\tpotential 240 Volts at 0.1 scale")
        if self._is_voltage_240(self._unsigned_mean, self._unsigned_max, 0.01):
            print(f"\tpotential 240 Volts at 0.01 scale")

        self._is_pv_voltage()


        """
        TODO: find what fluctuates with the sun (i.e. production)
        Zero until sunrise
        Rises until approximately local noon (depending on array pointing)
        Falls until sunset
        Zero after sunset
        
        """


        # TODO: find what fluctuates with people (i.e. usage)

        if self._is_percentage(self._data["value"],1):
            print(f"\tpercentage at scale 1.0, min {self._unsigned_min} max {self._unsigned_max}")
        else:    
            if self._is_percentage(self._data["value"],0.1):
                print(f"\tpercentage at scale 0.1, min {self._unsigned_min} max {self._unsigned_max}")
            else:
                if self._is_percentage(self._data["value"],0.01):
                    print(f"\tpercentage at scale 0.01, min {self._unsigned_min} max {self._unsigned_max}")


        self._daily_pattern()

        # TODO: fixed ranges

        #self._do_fft()

        return

    def _check_changing(self):
        """Check if values are changing."""
        if self._data["value"].max() == self._data["value"].min():
            self._changes = False
        else:
            self._changes = True

    def _check_zero(self):
        """Check if values are always zero."""
        if self.is_fixed() and self._data["value"].sum() == 0:
            self._zero == True
        else:
            self._zero == False

    def _check_increasing_decreasing(self):
        """Check if values are only increasing or only decreasing."""
        if self.is_changing():
            if self._data["value"].is_monotonic_increasing:
                self._increasing = True
                self._decreasing = False
            else:
                if self._data["value"].is_monotonic_decreasing:
                    self._increasing = False
                    self._decreasing = True

    def _is_voltage_120(self, mean, max, scale=1):
        """Return true if Voltage.
        mean is the average value of the register
        scale is the scaling factor (e.g. 1, .1, .01)
        """
        # looking for 120 or close to it.
        lower = 115/scale
        upper = 125/scale

        if max > upper:
            return False

        return mean >= lower and mean <= upper

    def _is_voltage_240(self, mean, max, scale=1):
        """Return true if Voltage.
        mean is the average value of the register
        scale is the scaling factor (e.g. 1, .1, .01)
        """
        # looking for 120 or close to it.
        lower = 235/scale
        upper = 245/scale

        if max > upper:
            return False

        return mean >= lower and mean <= upper        

    def _is_pv_voltage(self):
        """check if PV voltage."""
        if self._num_unique < 5:
            return

        if self._percent_in_range(self._data["value"], .75, 1.75, 1) > .99:
            print(f"\tpotential PV voltage at 1.0 scale")
        if self._percent_in_range(self._data["value"], .75, 1.75, .1) > .99:
            print(f"\tpotential PV voltage at .1 scale")
        if self._percent_in_range(self._data["value"],  .75, 1.75, .01) > .99:
            print(f"\tpotential PV voltage at .01 scale")
        return

    def _is_battery_voltage(self):
        """check if battery voltage ~54 Volts."""
        if self._num_unique < 5:
            return

        if self._percent_in_range(self._data["value"], 52, 56, 1) > .99:
            print(f"\tpotential battery voltage at 1.0 scale")
        if self._percent_in_range(self._data["value"], 52, 56, .1) > .99:
            print(f"\tpotential battery voltage at .1 scale")
        if self._percent_in_range(self._data["value"],  52, 56, .01) > .99:
            print(f"\tpotential battery voltage at .01 scale")
        return
        


    def _is_hertz(self, series, mean, scale=1):
        """Return true if Hertz.
        mean is the average value of the register
        scale is the scaling factor (e.g. 1, .1, .01)
        """
        if self._num_unique < MIN_UNIQUE_HERTZ:
            return False

        # between 0 and 60...with a little wiggle room
        if not self._values_in_range(series, 0, 62/scale):
            return False

        #print(f"percent in range (0,62): {self._percent_in_range(series, 0, 62/scale)}")
        # looking for 60 or close to it.
        lower = 58/scale
        upper = 62/scale

        return mean >= lower and mean <= upper

    def _is_percentage(self, series, scale=1):
        """Return true if Percentage.
        series is the series of values for the register
        scale is the scaling factor (e.g. 1, .1, .01)
        """
        # there must be many different values
        if self._num_unique < MIN_UNIQUE_PERCENT:
            return False

        # values must be within range
        #if not self._values_in_range(series, 0, 100/scale):
        #        return False

        if self._percent_in_range(series, 0, 100, scale) < .99:
                return False



        # the maximum value should be 100%
        #return series.max() == 100/scale
        return self._lenient_max(series, 0, 100/scale) == 100/scale

    def _lenient_max(self, series, min, max):
        """Return max value within a range (ignoring spurious values)"""
        maximum = 0
        for value in series:
            if value >= min and value <= max:
                if value > maximum:
                    maximum = value

        return maximum


    def _values_in_range(self, series, min, max):
        """Return true if all values are between min and max given."""
        for value in series:
            if value < min or value > max:
                return False
        return True

    def _percent_in_range(self, series, min, max, scale=1):
        """Return percentage of values between min and max given."""
        count = 0
        for value in series:
            if value >= min/scale and value <= max/scale:
                count +=1
        #print(f"percent in range: {count/len(series):.2%}")
        return count/len(series)




    def _daily_pattern(self):
        """Analyze daily pattern."""
        if not self.is_changing() or self._num_unique < 10:
            return False

        hourly = []
        # create a list of mean for each hour of the day
        for hour in range(24):
            hour_data = self._data[self._data["hour"] == hour]
            mean = hour_data["value"].mean()
            hourly.append(mean)
            if self._c_hour > .5:
                #print(f"{mean:5.1f}")
                pass

        self._daily_increasing(hourly)
        self._daily_with_sun(hourly)
        self._daily_with_sun2(hourly)
        self._daily_with_sun3(hourly)

        self._daily_decreases_without_sun(hourly)

        return True


    def _daily_increasing(self, hourly):
        """Return true if increases daily (from 0000 to 2400). Every hour >= last hour."""
        hour = 0
        last_mean = 0
        while hour < 24:
            if hour > 0:
                if hourly[hour] < last_mean:
                    return False
                last_mean = hourly[hour]

            hour +=1

        print("\tincreases daily from 0000 to 2400 (hourly mean)")
        return True

    def _daily_with_sun(self, hourly):
        """Return true if seems to increase with sun."""

        # increases in morning
        hour = 0
        last_mean = hourly[0]
        while hour < 12:
            if hourly[hour] < last_mean:
                return False
            last_mean = hourly[hour]

            hour +=1

        print("   made it this far...")

        # decreases in afternoon
        hour = 13
        last_mean = hourly[12]
        while hour < 24:
            if hourly[hour] > last_mean:
                return False
            last_mean = hourly[hour]

            hour +=1

        print("\tseems to increase with the sun")
        return True

    def _daily_with_sun2(self, hourly):
        """Return true if seems to increase with sun."""
        # if 5am value is same as midnight,
        print("\tno increase from midnight to 5am")
        return hourly[4] == hourly[0]

    def _daily_with_sun3(self, hourly):
        """Return true if seems to increase with sun."""
        # if 5am value is same as midnight,
        print("\tno increase from 10pm-midnight")
        return hourly[23] == hourly[22]

    def _daily_decreases_without_sun(self, hourly):
        """Return true if seems to decrease without sun."""

        # ensure it drops each hour
        hour = 21
        last_mean = hourly[20]
        while hour < 24:
            if hourly[hour] >= last_mean:
                return False
            last_mean = hourly[hour]
            hour +=1

        hour = 0
        while hour < 5:
            if hourly[hour] >= last_mean:
                return False
            last_mean = hourly[hour]
            hour +=1


        print("\tdecreases from 9pm to 6am")
        return True

    def _do_fft(self):
        """Do FFT stuff."""
        if self._num_unique < 10:
            return False

        data = rfft(self._data['value'])
        result = [abs(x) for x in data] 

        print(f"fft: {result[0]:5.1f}\t{result[1]:5.1f}\t{result[2]:5.1f}\t{result[3]:5.1f}")
        return True


    """
    GENERAL ISSUES

    Time - what time are the entries using?  Computer running script time?  Device/logger time?
    
    Noisy data?  Seems there are a few data values that are outside of the normal range (see #184 which seems a percentage, except for one or two data points)
    
    """