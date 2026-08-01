
def readcode(content):
    res = []
    for e in content_string(content).split("\n"):
        e = e.strip()
        if not len(e):
            continue
        res.append(e)
    return assemble(res)

