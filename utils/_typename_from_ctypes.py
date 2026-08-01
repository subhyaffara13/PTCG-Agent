
def _typename_from_ctypes(item):
    if item is None:
        return "void"
    elif item is ctypes.c_void_p:
        return "void *"

    name = item.__name__

    pointer_level = 0
    while name.startswith("LP_"):
        pointer_level += 1
        name = name[3:]

    if name.startswith('c_'):
        name = name[2:]

    if pointer_level > 0:
        name += " " + "*"*pointer_level

    return name

