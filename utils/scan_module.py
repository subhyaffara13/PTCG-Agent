
def scan_module(egg_dir, base, name, stubs):
    """Check whether module possibly uses unsafe-for-zipfile stuff"""

    filename = os.path.join(base, name)
    if filename[:-1] in stubs:
        return True  # Extension module
    pkg = base[len(egg_dir) + 1 :].replace(os.sep, '.')
    module = pkg + (pkg and '.' or '') + os.path.splitext(name)[0]
    skip = 16  # skip magic & reserved? & date & file size
    f = open(filename, 'rb')
    f.read(skip)
    code = marshal.load(f)
    f.close()
    safe = True
    symbols = dict.fromkeys(iter_symbols(code))
    for bad in ['__file__', '__path__']:
        if bad in symbols:
            log.warn("%s: module references %s", module, bad)
            safe = False
    if 'inspect' in symbols:
        for bad in [
            'getsource',
            'getabsfile',
            'getfile',
            'getsourcefile',
            'getsourcelines',
            'findsource',
            'getcomments',
            'getframeinfo',
            'getinnerframes',
            'getouterframes',
            'stack',
            'trace',
        ]:
            if bad in symbols:
                log.warn("%s: module MAY be using inspect.%s", module, bad)
                safe = False
    return safe

