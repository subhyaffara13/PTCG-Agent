
def nonblank(args):
    for line in args:
        line = trim(line)
        if line.isspace():
            continue
        yield line
    return

