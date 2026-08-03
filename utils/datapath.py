import os
from typing import Callable

def datapath(strict_data_files: str) -> Callable[..., str]:
    """
    Get the path to a data file.

    Parameters
    ----------
    path : str
        Path to the file, relative to ``pandas/tests/``

    Returns
    -------
    path including ``pandas/tests``.

    Raises
    ------
    ValueError
        If the path doesn't exist and the --no-strict-data-files option is not set.
    """
    BASE_PATH = os.path.join(os.path.dirname(__file__), "tests")

    def deco(*args):
        path = os.path.join(BASE_PATH, *args)
        if not os.path.exists(path):
            if strict_data_files:
                raise ValueError(
                    f"Could not find file {path} and --no-strict-data-files is not set."
                )
            pytest.skip(f"Could not find {path}.")
        return path

    return deco

