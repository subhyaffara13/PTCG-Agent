
def _calc_dual_canonical_window(win: np.ndarray, hop: int) -> np.ndarray:
    """Calculate canonical dual window for 1d window `win` and a time step
    of `hop` samples.

    A ``ValueError`` is raised if the inversion fails.

    This is a separate function not a method, since it is also used in the
    class method ``ShortTimeFFT.from_dual()``.
    """
    if hop > len(win):
        raise ValueError(f"{hop=} is larger than window length of {len(win)}" +
                         " => STFT not invertible!")
    if issubclass(win.dtype.type, np.integer):
        raise ValueError("Parameter 'win' cannot be of integer type, but " +
                         f"{win.dtype=} => STFT not invertible!")
        # The calculation of `relative_resolution` does not work for ints.
        # Furthermore, `win / DD` casts the integers away, thus an implicit
        # cast is avoided, which can always cause confusion when using 32-Bit
        # floats.

    w2 = win.real**2 + win.imag**2  # win*win.conj() does not ensure w2 is real
    DD = w2.copy()
    for k_ in range(hop, len(win), hop):
        DD[k_:] += w2[:-k_]
        DD[:-k_] += w2[k_:]

    # check DD > 0:
    relative_resolution = np.finfo(win.dtype).resolution * max(DD)
    if not np.all(DD >= relative_resolution):
        raise ValueError("Short-time Fourier Transform not invertible!")

    return win / DD

