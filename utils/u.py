
def U(name):
    """
    Get a unicode character by name or, None if not found.

    This exists because older versions of Python use older unicode databases.
    """
    try:
        return unicodedata.lookup(name)
    except KeyError:
        global unicode_warnings
        unicode_warnings += 'No \'%s\' in unicodedata\n' % name
        return None

