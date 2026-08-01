
def _module_init(state=None):
    # this is a sneaky dodge to store module level state in a non-public
    # function. Helps us dodge using globals.
    if state is not None:
        _module_init.value = state
        return state

    try:
        _module_init.value
    except AttributeError:
        return False
    return _module_init.value

