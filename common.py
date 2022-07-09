"""Common code."""

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
