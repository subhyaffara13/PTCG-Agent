
def _fftautocorr(x):
    """Compute the autocorrelation of a real array and crop the result."""
    N = x.shape[-1]
    use_N = sp_fft.next_fast_len(2*N-1)
    x_fft = sp_fft.rfft(x, use_N, axis=-1)
    cxy = sp_fft.irfft(x_fft * x_fft.conj(), n=use_N)[:, :N]
    # Or equivalently (but in most cases slower):
    # cxy = xp.asarray([xp.convolve(xx, yy[::-1], mode='full')
    #                   for xx, yy in zip(x, x)])[:, N-1:2*N-1]
    return cxy

