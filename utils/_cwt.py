
def _cwt(data, wavelet, widths, dtype=None, **kwargs):
    # Determine output type
    if dtype is None:
        if np.asarray(wavelet(1, widths[0], **kwargs)).dtype.char in 'FDG':
            dtype = np.complex128
        else:
            dtype = np.float64

    output = np.empty((len(widths), len(data)), dtype=dtype)
    for ind, width in enumerate(widths):
        N = np.min([10 * width, len(data)])
        wavelet_data = np.conj(wavelet(N, width, **kwargs)[::-1])
        output[ind] = convolve(data, wavelet_data, mode='same')
    return output

