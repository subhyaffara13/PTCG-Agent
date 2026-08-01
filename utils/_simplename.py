
def _simplename(name):
    """create simple version of the font name"""
    # return alphanumeric characters of a string (converted to lowercase)
    return "".join(c.lower() for c in name if c.isalnum())

