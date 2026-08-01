
def get_expected_input_dtype(func, xp):
    # use __name__ so that `lazy_xp_function` doesn't break things
    if func.__name__ in ["fft", "fftn", "fft2", "ifft", "ifftn", "ifft2", "hfft",
                         "hfftn", "hfft2", "irfft", "irfftn", "irfft2"]:
        dtype = xp.complex128
    elif func.__name__ in ["rfft", "rfftn", "rfft2", "ihfft", "ihfftn", "ihfft2"]:
        dtype = xp.float64
    else:
        raise ValueError(f'Unknown FFT function: {func}')

    return dtype

