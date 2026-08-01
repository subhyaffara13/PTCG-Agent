
def validate_all_hashable(*args, error_name: str | None = None) -> None:
    """
    Return None if all args are hashable, else raise a TypeError.

    Parameters
    ----------
    *args
        Arguments to validate.
    error_name : str, optional
        The name to use if error

    Raises
    ------
    TypeError : If an argument is not hashable

    Returns
    -------
    None
    """
    if not all(is_hashable(arg) for arg in args):
        if error_name:
            raise TypeError(f"{error_name} must be a hashable type")
        raise TypeError("All elements must be hashable")

