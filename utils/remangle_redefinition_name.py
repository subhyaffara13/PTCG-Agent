
def remangle_redefinition_name(name: str) -> str:
    """Remangle names produced by mypy when allow-redefinition-old is used and a name
    is used with multiple types within a single block.

    We only need to do this for locals, because the name is used as the name of the register;
    for globals, the name itself is stored in a register for the purpose of doing dict
    lookups.
    """
    return name.replace("'", "__redef__")

