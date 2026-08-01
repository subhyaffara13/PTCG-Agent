
def test_whittaker_reml(weights):
    """Test that whittaker with REML criterion works."""
    n = 10
    order = 2
    signal = np.sin(2*np.pi * np.linspace(0, 1, n))
    y = signal.copy()
    # add some (deterministic) noise
    y[::2] += 0.2
    y[1::2] -= 0.2
    w = None if weights is None else np.ones_like(y)

    wh = whittaker_henderson(y, lamb="reml", order=order, weights=w)
    assert wh.lamb > 0

    # Validate against R mgcv
    # library(mgcv)
    # n = 10
    # order = 2
    # signal = sin(2*pi * 0:(n-1) / (n-1))
    # y = signal
    # # add some (deterministic) noise
    # y[seq(1, n, 2)] = y[seq(1, n, 2)] + 0.2
    # y[seq(2, n, 2)] = y[seq(2, n, 2)] - 0.2
    # x <- 1:n
    # b <- gam(y ~ s(x, bs="ps", k=n, m=c(0, 2)), family = gaussian(),
    #          knots = list(x=0:11), method="REML",
    #          control = list(epsilon = 1e-12, mgcv.tol = 1e-12, efs.tol = 1e-12))
    # options(digits=12)
    # b$fitted.values
    expected = [
        0.209959334732, 0.589996568382, 0.938965773497, 0.766582291904, 0.349462653088,
        -0.349462653088, -0.766582291904, -0.938965773497, -0.589996568382,
        -0.209959334732,
    ]
    assert_allclose(wh.x, expected, rtol=1e-7)
    # b$sp
    expected_sp = 5.12904626508
    expected_sp /= 16  # not 100% sure how to justify this 16.
    assert wh.lamb == pytest.approx(expected_sp, rel=1e-7)

    # Double weights should result in double lamb.
    wh2 = whittaker_henderson(y, lamb="reml", order=order, weights=2 * np.ones_like(y))
    assert wh2.lamb == pytest.approx(2 * wh.lamb, rel=1e-7)

