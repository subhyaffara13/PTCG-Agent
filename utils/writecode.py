
def writecode(tag, writer, instrs):
    writer.begintag(tag)
    writer.newline()
    for l in disassemble(instrs):
        writer.write(l)
        writer.newline()
    writer.endtag(tag)
    writer.newline()

