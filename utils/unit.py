
def unit(request):
    """
    datetime64 units we support.
    """
    return request.param


def unit(key: str) -> str:
    """
    Unit in physical_constants indexed by key.

    Parameters
    ----------
    key : str
        Key in dictionary `physical_constants`

    Returns
    -------
    unit : str
        Unit in `physical_constants` corresponding to `key`

    Examples
    --------
    >>> from scipy import constants
    >>> constants.unit('proton mass')
    'kg'

    """
    _check_obsolete(key)
    return physical_constants[key][1]

