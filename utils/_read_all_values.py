
def _read_all_values(data, used=0):
    """Yield (key, value, timestamp, pos). No locking is performed."""

    if used <= 0:
        # If not valid `used` value is passed in, read it from the file.
        used = _unpack_integer(data, 0)[0]

    pos = 8

    while pos < used:
        encoded_len = _unpack_integer(data, pos)[0]
        # check we are not reading beyond bounds
        if encoded_len + pos > used:
            raise RuntimeError('Read beyond file size detected, file is corrupted.')
        pos += 4
        encoded_key = data[pos:pos + encoded_len]
        padded_len = encoded_len + (8 - (encoded_len + 4) % 8)
        pos += padded_len
        value, timestamp = _unpack_two_doubles(data, pos)
        yield encoded_key.decode('utf-8'), value, timestamp, pos
        pos += 16

