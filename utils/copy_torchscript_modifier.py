
def copy_torchscript_modifier(orig, new) -> None:
    attr = get_torchscript_modifier(orig)
    if attr is None:
        return
    new._torchscript_modifier = attr

