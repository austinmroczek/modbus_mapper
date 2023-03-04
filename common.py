"""Common code."""

import string
from datetime import datetime

class Value:

    value = 0
    byte1 = 0
    byte2 = 0
    changed = 0
    num_changes = 0
    zero = 1
    char1 = ""
    char2 = ""

    def __init__(self, new_register, new_value):
        self.register = new_register
        self._set(new_value)

    def update(self, new_value):
        if self.value != new_value:
            self.changed = 1
            self.num_changes += 1
            self._set(new_value)

    def _set(self, new_value):
        self.value = new_value
        self.byte1 = new_value & 0xff
        self.byte2 = new_value >> 8
        self.char1 = chr(self.byte1)
        self.char2 = chr(self.byte2)
        if new_value != 0:
            self.zero = 0

class Address:
    """Hold info for an address."""

    address = 0
    _value = None
    byte1 = None
    byte2 = None
    char1 = None
    char2 = None
    is_fixed = False
    is_zero = False
    is_increasing = False
    is_decreasing = False
    is_ascii = False
    unsigned_max = None
    unsigned_min = None
    unsigned_mean = None
    unsigned_median = None
    unsigned_mode = None
    signed_max = None
    signed_min = None
    signed_mean = None
    signed_median = None

    c_year = None
    c_month = None
    c_day_of_month = None
    c_day_of_year = None
    c_day_of_week = None
    c_hour = None
    c_minute = None


    def __init__(self, address):
        """Initiate with an address."""
        self.address = address

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

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):

        new_value = int(new_value)
        self._value = new_value
        self.byte1 = new_value & 0xff
        self.byte2 = new_value >> 8
        self.char1 = chr(self.byte1)
        self.char2 = chr(self.byte2)

        if self.char1 in string.printable and self.char2 in string.printable:
            self.is_ascii = True

