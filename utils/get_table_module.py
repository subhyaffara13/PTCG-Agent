
def getTableModule(tag: str | bytes) -> ModuleType | None:
    """Fetch the packer/unpacker module for a table.
    Return None when no module is found.
    """
    from . import tables

    pyTag = tagToIdentifier(tag)
    try:
        __import__("fontTools.ttLib.tables." + pyTag)
    except ImportError as err:
        # If pyTag is found in the ImportError message,
        # means table is not implemented.  If it's not
        # there, then some other module is missing, don't
        # suppress the error.
        if str(err).find(pyTag) >= 0:
            return None
        else:
            raise err
    else:
        return getattr(tables, pyTag)

