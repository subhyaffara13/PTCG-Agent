
def maybe_skip_size_asserts(op):
    """
    For certain ops, there meta and eager implementation returns different
    strides. This cause size/strides assert fail. Skip adding those
    asserts for now.
    """
    if (
        op.aten_name
        in (
            "fft_hfftn",
            "fft_hfft",
            "fft_hfft2",
            "fft_ihfftn",
            "fft_fft",
            "fft_fft2",
            "fft_fftn",
            "fft_ifft",
            "fft_ifft2",
            "fft_ifftn",
            "fft_irfft",
            "fft_irfft2",
            "fft_irfftn",
            "fft_ihfft",
            "fft_ihfft2",
            "fft_rfft",
            "fft_rfft2",
            "fft_rfftn",
            "linalg_eig",
            "linalg_eigvals",
        )
        and "TORCHINDUCTOR_SIZE_ASSERTS" not in os.environ
    ):
        return torch._inductor.config.patch(size_asserts=False)
    else:
        return contextlib.nullcontext()

