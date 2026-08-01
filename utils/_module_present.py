
def _module_present(modname, modlist):
    if modname in modlist:
        return True
    for m in modlist:
        if hasattr(m, '__name__') and m.__name__ == modname:
            return True
    return False

