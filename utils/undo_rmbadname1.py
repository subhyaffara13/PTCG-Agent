
def undo_rmbadname1(name):
    if name in invbadnames:
        errmess(f'undo_rmbadname1: Replacing "{name}" with "{invbadnames[name]}".\n')
        return invbadnames[name]
    return name

