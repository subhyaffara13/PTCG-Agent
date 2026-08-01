
def load_source(file, **kwds):
    """load an object that was stored with dill.temp.dump_source

    file: filehandle
    alias: string name of stored object
    mode: mode to open the file, one of: {'r', 'rb'}

    >>> f = lambda x: x**2
    >>> pyfile = dill.temp.dump_source(f, alias='_f')
    >>> _f = dill.temp.load_source(pyfile)
    >>> _f(4)
    16
    """
    alias = kwds.pop('alias', None)
    mode = kwds.pop('mode', 'r')
    fname = getattr(file, 'name', file) # fname=file.name or fname=file (if str)
    source = open(fname, mode=mode, **kwds).read()
    if not alias:
        tag = source.strip().splitlines()[-1].split()
        if tag[0] != '#NAME:':
            stub = source.splitlines()[0]
            raise IOError("unknown name for code: %s" % stub)
        alias = tag[-1]
    local = {}
    exec(source, local)
    _ = eval("%s" % alias, local)
    return _

