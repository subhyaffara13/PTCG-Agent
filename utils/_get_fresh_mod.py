
def _get_fresh_mod():
    # Get this module, with warning registry empty
    my_mod = sys.modules[__name__]
    try:
        my_mod.__warningregistry__.clear()
    except AttributeError:
        # will not have a __warningregistry__ unless warning has been
        # raised in the module at some point
        pass
    return my_mod

