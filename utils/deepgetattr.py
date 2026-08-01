
def deepgetattr(obj, attr):
    """Recurses through an attribute chain to get the ultimate value."""
    for key in attr.split("."):
        obj = getattr(obj, key)
    return obj

