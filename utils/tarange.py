
def tarange(*args, **kwargs):
    """
    A shortcut for `tqdm.asyncio.tqdm(range(*args), **kwargs)`.
    """
    return tqdm_asyncio(range(*args), **kwargs)

