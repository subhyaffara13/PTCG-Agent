
def test_gh12696():
    # Test that optimize doesn't throw warning gh-12696
    with assert_no_warnings():
        optimize.fminbound(
            lambda x: np.array([x**2]), -np.pi, np.pi, disp=False)

