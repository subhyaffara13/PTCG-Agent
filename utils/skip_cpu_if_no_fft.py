
def skipCPUIfNoFFT(fn):
    return skipCPUIf(not torch._C.has_spectral, "PyTorch is built without FFT support")(
        fn
    )

