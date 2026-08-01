
def listToRegexpStr(charList):
    rv = []
    for item in charList:
        if item[0] == item[1]:
            rv.append(escapeRegexp(chr(item[0])))
        else:
            rv.append(escapeRegexp(chr(item[0])) + "-" +
                      escapeRegexp(chr(item[1])))
    return "[%s]" % "".join(rv)

