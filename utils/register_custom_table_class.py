
def registerCustomTableClass(
    tag: str | bytes, moduleName: str, className: str | None = None
) -> None:
    """Register a custom packer/unpacker class for a table.

    The 'moduleName' must be an importable module. If no 'className'
    is given, it is derived from the tag, for example it will be
    ``table_C_U_S_T_`` for a 'CUST' tag.

    The registered table class should be a subclass of
    :py:class:`fontTools.ttLib.tables.DefaultTable.DefaultTable`
    """
    if className is None:
        className = "table_" + tagToIdentifier(tag)
    _customTableRegistry[tag] = (moduleName, className)

