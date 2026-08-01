
def get_workers():
    """Returns the default number of workers within the current context.

    Returns
    -------
    n_workers : int
        The default number of workers

    Examples
    --------
    >>> from scipy import fft
    >>> fft.get_workers()
    1
    >>> with fft.set_workers(4):
    ...     fft.get_workers()
    4
    """
    return getattr(_config, 'default_workers', 1)

