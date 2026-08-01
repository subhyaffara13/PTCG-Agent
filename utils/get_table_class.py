
def getTableClass(tag: str | bytes) -> type[DefaultTable]:
    """Fetch the packer/unpacker class for a table."""
    tableClass = getCustomTableClass(tag)
    if tableClass is not None:
        return tableClass
    module = getTableModule(tag)
    if module is None:
        from .tables.DefaultTable import DefaultTable

        return DefaultTable
    pyTag = tagToIdentifier(tag)
    tableClass = getattr(module, "table_" + pyTag)
    return tableClass

