
def has_module(module):
    """
    Return True if module exists, otherwise run skip().

    module should be a string.
    """
    # To give a string of the module name to skip(), this function takes a
    # string.  So we don't waste time running import_module() more than once,
    # just map the three modules tested here in this dict.
    modnames = {'numpy': numpy, 'Cython': Cython, 'f2py': f2py}

    if modnames[module]:
        if module == 'f2py' and not f2pyworks:
            skip("Couldn't run f2py.")
        return True
    skip("Couldn't import %s." % module)

