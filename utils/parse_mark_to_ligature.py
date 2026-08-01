
def parseMarkToLigature(lines, font, _lookupMap=None):
    return parseMarkToSomething(lines, font, MarkToLigatureHelper())

