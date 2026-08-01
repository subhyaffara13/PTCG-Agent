
def _align_32(f):
    '''Align to the next 32-bit position in a file'''

    pos = f.tell()
    if pos % 4 != 0:
        f.seek(pos + 4 - pos % 4)
    return

