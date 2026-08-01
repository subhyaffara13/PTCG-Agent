
def ttgrange(*args, **kwargs):
    """Shortcut for `tqdm.contrib.telegram.tqdm(range(*args), **kwargs)`."""
    return tqdm_telegram(range(*args), **kwargs)

