
def trrange(*args, **kwargs):
    """Shortcut for `tqdm.rich.tqdm(range(*args), **kwargs)`."""
    return tqdm_rich(range(*args), **kwargs)

