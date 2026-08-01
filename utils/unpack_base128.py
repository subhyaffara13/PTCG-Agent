
def unpackBase128(data):
    r"""Read one to five bytes from UIntBase128-encoded input string, and return
    a tuple containing the decoded integer plus any leftover data.

    >>> unpackBase128(b'\x3f\x00\x00') == (63, b"\x00\x00")
    True
    >>> unpackBase128(b'\x8f\xff\xff\xff\x7f')[0] == 4294967295
    True
    >>> unpackBase128(b'\x80\x80\x3f')  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    TTLibError: UIntBase128 value must not start with leading zeros
    >>> unpackBase128(b'\x8f\xff\xff\xff\xff\x7f')[0]  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    TTLibError: UIntBase128-encoded sequence is longer than 5 bytes
    >>> unpackBase128(b'\x90\x80\x80\x80\x00')[0]  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      File "<stdin>", line 1, in ?
    TTLibError: UIntBase128 value exceeds 2**32-1
    """
    if len(data) == 0:
        raise TTLibError("not enough data to unpack UIntBase128")
    result = 0
    if byteord(data[0]) == 0x80:
        # font must be rejected if UIntBase128 value starts with 0x80
        raise TTLibError("UIntBase128 value must not start with leading zeros")
    for i in range(woff2Base128MaxSize):
        if len(data) == 0:
            raise TTLibError("not enough data to unpack UIntBase128")
        code = byteord(data[0])
        data = data[1:]
        # if any of the top seven bits are set then we're about to overflow
        if result & 0xFE000000:
            raise TTLibError("UIntBase128 value exceeds 2**32-1")
        # set current value = old value times 128 bitwise-or (byte bitwise-and 127)
        result = (result << 7) | (code & 0x7F)
        # repeat until the most significant bit of byte is false
        if (code & 0x80) == 0:
            # return result plus left over data
            return result, data
    # make sure not to exceed the size bound
    raise TTLibError("UIntBase128-encoded sequence is longer than 5 bytes")

