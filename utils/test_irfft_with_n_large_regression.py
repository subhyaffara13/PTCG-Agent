
def test_irfft_with_n_large_regression():
    # Regression test for gh-25679
    x = np.arange(5) * (1 + 1j)
    result = np.fft.hfft(x, n=10)
    expected = np.array([20., 9.91628173, -11.8819096, 7.1048486,
                         -6.62459848, 4., -3.37540152, -0.16057669,
                         1.8819096, -20.86055364])
    assert_allclose(result, expected)

