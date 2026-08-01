
def tgrange(*args, **kwargs):
    """Shortcut for `tqdm.gui.tqdm(range(*args), **kwargs)`."""
    return tqdm_gui(range(*args), **kwargs)

