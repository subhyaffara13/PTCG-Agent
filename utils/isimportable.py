
def isimportable(name):
    if name and (name[0].isalpha() or name[0] == "_"):
        name = name.replace("_", "")
        return not name or name.isalnum()

