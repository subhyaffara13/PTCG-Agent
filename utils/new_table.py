
def newTable(tag: str | bytes) -> DefaultTable:
    """Return a new instance of a table."""
    tableClass = getTableClass(tag)
    return tableClass(tag)

