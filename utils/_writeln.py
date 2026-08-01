
def _writeln(fh, line):
    # Ending lines with a % prevents TeX from inserting spurious spaces
    # (https://tex.stackexchange.com/questions/7453).
    fh.write(line)
    fh.write("%\n")

