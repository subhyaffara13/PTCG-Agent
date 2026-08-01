
def wrapline(writer, dat, length=80):
    currline = ""
    for d in dat:
        if len(currline) > length:
            writer.write(currline[:-1])
            writer.newline()
            currline = ""
        currline += d + " "
    if len(currline):
        writer.write(currline[:-1])
        writer.newline()

