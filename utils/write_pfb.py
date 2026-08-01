
def writePFB(path, data):
    chunks = findEncryptedChunks(data)
    with open(path, "wb") as f:
        for isEncrypted, chunk in chunks:
            if isEncrypted:
                code = 2
            else:
                code = 1
            f.write(bytechr(128) + bytechr(code))
            f.write(longToString(len(chunk)))
            f.write(chunk)
        f.write(bytechr(128) + bytechr(3))

