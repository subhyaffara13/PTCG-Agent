
def _repr(obj):
    """
    Get the representation of an object, with dedicated pprint-like format for lists.
    """
    if isinstance(obj, list):
        return "[" + (",\n ".join((_repr(e).replace("\n", "\n ") for e in obj))) + "\n]"
    else:
        return repr(obj)

