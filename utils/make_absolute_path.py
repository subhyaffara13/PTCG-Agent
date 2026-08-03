import pathlib

def make_absolute_path(partial_path: str) -> str:
    """Convert a partial path to an absolute path.

    A path such a `sympy/core` might be needed. However, absolute paths should
    be used in the arguments to pytest in all cases as it avoids errors that
    arise from nonexistent paths.

    This function assumes that partial_paths will be passed in such that they
    begin with the explicit `sympy` directory, i.e. `sympy/...`.

    """

    def is_valid_partial_path(partial_path: str) -> bool:
        """Assumption that partial paths are defined from the `sympy` root."""
        return pathlib.Path(partial_path).parts[0] == 'sympy'

    if not is_valid_partial_path(partial_path):
        msg = (
            f'Partial path {dir(partial_path)} is invalid, partial paths are '
            f'expected to be defined with the `sympy` directory as the root.'
        )
        raise ValueError(msg)

    absolute_path = str(pathlib.Path(sympy_dir(), partial_path))
    return absolute_path

