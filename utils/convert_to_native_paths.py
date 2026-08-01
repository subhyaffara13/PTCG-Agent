
def convert_to_native_paths(lst):
    """
    Converts a list of '/' separated paths into a list of
    native (os.sep separated) paths and converts to lowercase
    if the system is case insensitive.
    """
    newlst = []
    for rv in lst:
        rv = os.path.join(*rv.split("/"))
        # on windows the slash after the colon is dropped
        if sys.platform == "win32":
            pos = rv.find(':')
            if pos != -1:
                if rv[pos + 1] != '\\':
                    rv = rv[:pos + 1] + '\\' + rv[pos + 1:]
        newlst.append(os.path.normcase(rv))
    return newlst

