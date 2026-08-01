
def test_intermediate_overlow():
    # Make sure we avoid overflow in situations where cosh/sinh would
    # overflow but the product with sin/cos would not
    sinpi_pts = [complex(1 + 1e-14, 227),
                 complex(1e-35, 250),
                 complex(1e-301, 445)]
    # Data generated with mpmath
    sinpi_std = [complex(-8.113438309924894e+295, -np.inf),
                 complex(1.9507801934611995e+306, np.inf),
                 complex(2.205958493464539e+306, np.inf)]
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "invalid value encountered in multiply", RuntimeWarning)
        for p, std in zip(sinpi_pts, sinpi_std):
            res = sinpi(p)
            assert_allclose(res.real, std.real)
            assert_allclose(res.imag, std.imag)

    # Test for cosine, less interesting because cos(0) = 1.
    p = complex(0.5 + 1e-14, 227)
    std = complex(-8.113438309924894e+295, -np.inf)
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "invalid value encountered in multiply", RuntimeWarning)
        res = cospi(p)
        assert_allclose(res.real, std.real)
        assert_allclose(res.imag, std.imag)

