
def is_decodable(value):
    r"""
    Return True if the supplied value is decodable (using the default
    encoding).

    >>> is_decodable(b'\xff')
    False
    >>> is_decodable(b'\x32')
    True
    """
    value.decode()

