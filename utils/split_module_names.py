
def split_module_names(mod_name: str) -> list[str]:
    """Return the module and all parent module names.

    So, if `mod_name` is 'a.b.c', this function will return
    ['a.b.c', 'a.b', and 'a'].
    """
    out = [mod_name]
    while "." in mod_name:
        mod_name = mod_name.rsplit(".", 1)[0]
        out.append(mod_name)
    return out

