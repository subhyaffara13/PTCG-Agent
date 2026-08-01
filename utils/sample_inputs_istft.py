
def sample_inputs_istft(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def mt(shape, **kwargs):
        real_shape = shape if dtype.is_complex else shape + (2,)
        return make_arg(real_shape, **kwargs)

    yield SampleInput(mt((10, 2)), kwargs=dict(n_fft=10))
    yield SampleInput(mt((6, 3)), kwargs=dict(n_fft=6, onesided=False))
    yield SampleInput(mt((6, 4)), kwargs=dict(n_fft=10, onesided=True))

    for center in [False, True]:
        yield SampleInput(mt((10, 10, 6)), kwargs=dict(n_fft=10, center=center))
        yield SampleInput(mt((1, 9, 10)), kwargs=dict(n_fft=16, hop_length=4, center=center))

    window = make_arg(10, low=.5, high=2.0)
    yield SampleInput(mt((10, 10, 6)), kwargs=dict(
        n_fft=10, window=window, center=center, return_complex=dtype.is_complex))
    yield SampleInput(mt((10, 10, 10)), kwargs=dict(
        n_fft=10, window=window[:8], win_length=8, center=center, return_complex=True))

    real_window = window if not dtype.is_complex else window.real
    yield SampleInput(mt((10, 5, 6)), kwargs=dict(n_fft=8, window=real_window[:8], center=center))

