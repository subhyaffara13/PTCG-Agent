
def test_rel_entr_gh_20710_near_zero():
    # Check accuracy of inputs which are very close
    inputs = np.array([
        # x, y
        (0.9456657713430001, 0.9456657713430094),
        (0.48066098564791515, 0.48066098564794774),
        (0.786048657854401, 0.7860486578542367),
    ])
    # Known values produced using `x * mpmath.log(x / y)` with dps=30
    expected = [
        -9.325873406851269e-15,
        -3.258504577274724e-14,
        1.6431300764454033e-13,
    ]
    x = inputs[:, 0]
    y = inputs[:, 1]
    assert_allclose(special.rel_entr(x, y), expected, rtol=1e-13, atol=0)

