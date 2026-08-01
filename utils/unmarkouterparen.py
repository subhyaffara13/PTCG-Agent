
def unmarkouterparen(line):
    r = line.replace('@(@', '(').replace('@)@', ')')
    return r

