
def containsderivedtypes(rout):
    if hasderivedtypes(rout):
        return 1
    if hasbody(rout):
        for b in rout['body']:
            if hasderivedtypes(b):
                return 1
    return 0

