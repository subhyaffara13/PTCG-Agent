
def writeLWFN(path, data):
    # Res.FSpCreateResFile was deprecated in OS X 10.5
    Res.FSpCreateResFile(path, "just", "LWFN", 0)
    resRef = Res.FSOpenResFile(path, 2)  # write-only
    try:
        Res.UseResFile(resRef)
        resID = 501
        chunks = findEncryptedChunks(data)
        for isEncrypted, chunk in chunks:
            if isEncrypted:
                code = 2
            else:
                code = 1
            while chunk:
                res = Res.Resource(bytechr(code) + "\0" + chunk[: LWFNCHUNKSIZE - 2])
                res.AddResource("POST", resID, "")
                chunk = chunk[LWFNCHUNKSIZE - 2 :]
                resID = resID + 1
        res = Res.Resource(bytechr(5) + "\0")
        res.AddResource("POST", resID, "")
    finally:
        Res.CloseResFile(resRef)

