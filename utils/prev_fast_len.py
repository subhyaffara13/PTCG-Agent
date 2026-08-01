
def prev_fast_len(target, real=False):
    """Find the previous fast size of input data to ``fft``.
    Useful for discarding a minimal number of samples before FFT.

    SciPy's FFT algorithms gain their speed by a recursive divide and conquer
    strategy. This relies on efficient functions for small prime factors of the
    input length. Thus, the transforms are fastest when using composites of the
    prime factors handled by the fft implementation. If there are efficient
    functions for all radices <= `n`, then the result will be a number `x`
    <= ``target`` with only prime factors <= `n`. (Also known as `n`-smooth
    numbers)

    Parameters
    ----------
    target : int
        Maximum length to search until. Must be a positive integer.
    real : bool, optional
        True if the FFT involves real input or output (e.g., `rfft` or `hfft`
        but not `fft`). Defaults to False.

    Returns
    -------
    out : int
        The largest fast length less than or equal to ``target``.

    Notes
    -----
    The result of this function may change in future as performance
    considerations change, for example, if new prime factors are added.

    Calling `fft` or `ifft` with real input data performs an ``'R2C'``
    transform internally.

    In the current implementation, prev_fast_len assumes radices of
    2,3,5,7,11 for complex FFT and 2,3,5 for real FFT.

    Examples
    --------
    On a particular machine, an FFT of prime length takes 16.2 ms:

    >>> from scipy import fft
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> max_len = 93059  # prime length is worst case for speed
    >>> a = rng.standard_normal(max_len)
    >>> b = fft.fft(a)

    Performing FFT on the maximum fast length less than max_len
    reduces the computation time to 1.5 ms, a speedup of 10.5 times:

    >>> fft.prev_fast_len(max_len, real=True)
    92160
    >>> c = fft.fft(a[:92160]) # discard last 899 samples

    """
    pass

