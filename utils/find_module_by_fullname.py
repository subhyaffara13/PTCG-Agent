
def find_module_by_fullname(fullname: str, modules: dict[str, State]) -> State | None:
    """Find module by a node fullname.

    This logic mimics the one we use in fixup, so should be good enough.
    """
    head = fullname
    # Special case: a module symbol is considered to be defined in itself, not in enclosing
    # package, since this is what users want when clicking go to definition on a module.
    if head in modules:
        return modules[head]
    while True:
        if "." not in head:
            return None
        head, tail = head.rsplit(".", maxsplit=1)
        mod = modules.get(head)
        if mod is not None:
            return mod

