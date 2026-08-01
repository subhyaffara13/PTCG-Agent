
def format_four_bytes(num):
    return '\\x%02X\\x%02X\\x%02X\\x%02X' % (
        (num >> 24) & 0xFF,
        (num >> 16) & 0xFF,
        (num >>  8) & 0xFF,
        (num      ) & 0xFF)

