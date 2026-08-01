
def readPlistFromString(data):
    return loads(tobytes(data, encoding="utf-8"), use_builtin_types=False)

