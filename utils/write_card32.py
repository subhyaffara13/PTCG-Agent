
def writeCard32(file, value):
    file.write(struct.pack(">L", value))

