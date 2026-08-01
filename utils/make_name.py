
def makeName(string, nameID, platformID, platEncID, langID):
    name = NameRecord()
    name.string, name.nameID, name.platformID, name.platEncID, name.langID = (
        string,
        nameID,
        platformID,
        platEncID,
        langID,
    )
    return name

