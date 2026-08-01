
def writeCard16(file, value):
    file.write(struct.pack(">H", value))

