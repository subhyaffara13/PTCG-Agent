
def precision(key: str) -> float:
    """
    Relative precision in physical_constants indexed by key.

    Parameters
    ----------
    key : str
        Key in dictionary `physical_constants`

    Returns
    -------
    prec : float
        Relative precision in `physical_constants` corresponding to `key`

    Examples
    --------
    >>> from scipy import constants
    >>> constants.precision('proton mass')
    5.1e-37

    """
    _check_obsolete(key)
    return physical_constants[key][2] / physical_constants[key][0]

