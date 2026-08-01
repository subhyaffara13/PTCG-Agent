
def save_module_dict(pickler, obj):
    if is_dill(pickler, child=False) and obj == pickler._main.__dict__ and \
            not (pickler._session and pickler._first_pass):
        logger.trace(pickler, "D1: %s", _repr_dict(obj)) # obj
        pickler.write(bytes('c__builtin__\n__main__\n', 'UTF-8'))
        logger.trace(pickler, "# D1")
    elif (not is_dill(pickler, child=False)) and (obj == _main_module.__dict__):
        logger.trace(pickler, "D3: %s", _repr_dict(obj)) # obj
        pickler.write(bytes('c__main__\n__dict__\n', 'UTF-8'))  #XXX: works in general?
        logger.trace(pickler, "# D3")
    elif '__name__' in obj and obj != _main_module.__dict__ \
            and type(obj['__name__']) is str \
            and obj is getattr(_import_module(obj['__name__'],True), '__dict__', None):
        logger.trace(pickler, "D4: %s", _repr_dict(obj)) # obj
        pickler.write(bytes('c%s\n__dict__\n' % obj['__name__'], 'UTF-8'))
        logger.trace(pickler, "# D4")
    else:
        logger.trace(pickler, "D2: %s", _repr_dict(obj)) # obj
        if is_dill(pickler, child=False) and pickler._session:
            # we only care about session the first pass thru
            pickler._first_pass = False
        StockPickler.save_dict(pickler, obj)
        logger.trace(pickler, "# D2")
    return

