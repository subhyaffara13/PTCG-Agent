
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def remove_prefix(text, prefix):
    """
    Remove the prefix from the text if it exists.

    >>> remove_prefix('underwhelming performance', 'underwhelming ')
    'performance'

    >>> remove_prefix('something special', 'sample')
    'something special'
    """
    null, prefix, rest = text.rpartition(prefix)
    return rest

