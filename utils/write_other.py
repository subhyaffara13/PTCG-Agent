
def writeOther(path, data, dohex=False):
    chunks = findEncryptedChunks(data)
    with open(path, "wb") as f:
        hexlinelen = HEXLINELENGTH // 2
        for isEncrypted, chunk in chunks:
            if isEncrypted:
                code = 2
            else:
                code = 1
            if code == 2 and dohex:
                while chunk:
                    f.write(eexec.hexString(chunk[:hexlinelen]))
                    f.write(b"\r")
                    chunk = chunk[hexlinelen:]
            else:
                f.write(chunk)

