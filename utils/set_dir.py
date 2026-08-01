
def set_dir(d: str | os.PathLike) -> None:
    r"""
    Optionally set the Torch Hub directory used to save downloaded models & weights.

    Args:
        d (str): path to a local folder to save downloaded models & weights.
    """
    global _hub_dir
    _hub_dir = os.path.expanduser(d)

