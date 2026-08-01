
def rmbadname1(name):
    if name in badnames:
        errmess(f'rmbadname1: Replacing "{name}" with "{badnames[name]}".\n')
        return badnames[name]
    return name

