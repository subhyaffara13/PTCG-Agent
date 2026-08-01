
def parse_environ_block(data):
    """Parse a C environ block of environment variables into a dictionary."""
    # The block is usually raw data from the target process.  It might contain
    # trailing garbage and lines that do not look like assignments.
    ret = {}
    pos = 0

    # localize global variable to speed up access.
    WINDOWS_ = WINDOWS
    while True:
        next_pos = data.find("\0", pos)
        # nul byte at the beginning or double nul byte means finish
        if next_pos <= pos:
            break
        # there might not be an equals sign
        equal_pos = data.find("=", pos, next_pos)
        if equal_pos > pos:
            key = data[pos:equal_pos]
            value = data[equal_pos + 1 : next_pos]
            # Windows expects environment variables to be uppercase only
            if WINDOWS_:
                key = key.upper()
            ret[key] = value
        pos = next_pos + 1

    return ret

