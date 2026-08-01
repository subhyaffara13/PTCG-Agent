
def _imp(*args, **kwds):
    """
    Replaces the default __import__, to allow a module to be memorised
    before the user can change it
    """
    before = set(sys.modules.keys())
    mod = __import__(*args, **kwds)
    after = set(sys.modules.keys()).difference(before)
    for m in after:
        memorise(sys.modules[m])
    return mod

