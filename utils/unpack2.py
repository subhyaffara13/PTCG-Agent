
def unpack2(fmt, data, obj=None):
    length = calcsize(fmt)
    return unpack(fmt, data[:length], obj), data[length:]

