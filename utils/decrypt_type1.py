
def decryptType1(data):
    chunks = findEncryptedChunks(data)
    data = []
    for isEncrypted, chunk in chunks:
        if isEncrypted:
            if isHex(chunk[:4]):
                chunk = deHexString(chunk)
            decrypted, R = eexec.decrypt(chunk, 55665)
            decrypted = decrypted[4:]
            if (
                decrypted[-len(EEXECINTERNALEND) - 1 : -1] != EEXECINTERNALEND
                and decrypted[-len(EEXECINTERNALEND) - 2 : -2] != EEXECINTERNALEND
            ):
                raise T1Error("invalid end of eexec part")
            decrypted = decrypted[: -len(EEXECINTERNALEND) - 2] + b"\r"
            data.append(EEXECBEGINMARKER + decrypted + EEXECENDMARKER)
        else:
            if chunk[-len(EEXECBEGIN) - 1 : -1] == EEXECBEGIN:
                data.append(chunk[: -len(EEXECBEGIN) - 1])
            else:
                data.append(chunk)
    return bytesjoin(data)

