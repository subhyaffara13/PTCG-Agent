
def demangle(name: str) -> str:
    """
    Note: Unlike PackageMangler.demangle, this version works on any
    mangled name, irrespective of which PackageMangler created it.
    """
    if is_mangled(name):
        _first, sep, last = name.partition(".")
        # If there is only a base mangle prefix, e.g. '<torch_package_0>',
        # then return an empty string.
        return last if len(sep) != 0 else ""
    return name

