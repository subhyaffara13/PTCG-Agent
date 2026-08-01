
def tnrange(*args, **kwargs):
    """Shortcut for `tqdm.notebook.tqdm(range(*args), **kwargs)`."""
    return tqdm_notebook(range(*args), **kwargs)


def tnrange(*args, **kwargs):  # pragma: no cover
    """Shortcut for `tqdm.notebook.tqdm(range(*args), **kwargs)`."""
    from warnings import warn

    from .notebook import trange as _tnrange
    warn("Please use `tqdm.notebook.trange` instead of `tqdm.tnrange`",
         TqdmDeprecationWarning, stacklevel=2)
    return _tnrange(*args, **kwargs)

