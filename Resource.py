from enum import Flag

class Resource(Flag):
    EMPTY = 0
    LOADED = 1
    CREATED = 2

    def set(self, flag, bit):
        flag |= bit

    def unset(self, flag, bit):
        flag &= ~bit
