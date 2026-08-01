
def remove_suffix(text, suffix):
    """
    Remove the suffix from the text if it exists.

    >>> remove_suffix('name.git', '.git')
    'name'

    >>> remove_suffix('something special', 'sample')
    'something special'
    """
    rest, suffix, null = text.partition(suffix)
    return rest

