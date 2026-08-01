
def getClassTag(klass: type[DefaultTable]) -> str | bytes:
    """Fetch the table tag for a class object."""
    name = klass.__name__
    assert name[:6] == "table_"
    name = name[6:]  # Chop 'table_'
    return identifierToTag(name)

