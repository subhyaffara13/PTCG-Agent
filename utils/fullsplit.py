
def fullsplit(line):
    words = line.split()
    rest = ' '.join(words[1:])
    return fixcommand(words[0]), [s.strip() for s in rest.split(',')]

