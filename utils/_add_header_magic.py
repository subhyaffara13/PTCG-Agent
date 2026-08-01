
def _add_header_magic(data):
    # Add b"PAR1" to file headers
    for path in list(data):
        add_magic = True
        for k in data[path]:
            if k[0] == 0 and k[1] >= 4:
                add_magic = False
                break
        if add_magic:
            data[path][(0, 4)] = b"PAR1"

