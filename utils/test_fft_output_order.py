
def test_fft_output_order(order, n):
    rng = np.random.RandomState(42)
    x = rng.rand(10)
    x = np.asarray(x, dtype=np.complex64, order=order)
    res = np.fft.fft(x, n=n)
    assert res.flags.c_contiguous == x.flags.c_contiguous
    assert res.flags.f_contiguous == x.flags.f_contiguous

