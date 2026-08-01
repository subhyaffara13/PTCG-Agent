
def test_deprecation():
    with pytest.warns(DeprecationWarning):
        linprog(1, method='interior-point')
    with pytest.warns(DeprecationWarning):
        linprog(1, method='revised simplex')
    with pytest.warns(DeprecationWarning):
        linprog(1, method='simplex')


def test_deprecation():
    """Test that access to previous attributes still works."""
    # This should be accessible immediately from scipy.io import
    with assert_warns(DeprecationWarning):
        scipy.io.matlab.mio5_params.MatlabOpaque

    # These should be importable but warn as well
    with assert_warns(DeprecationWarning):
        from scipy.io.matlab.miobase import MatReadError  # noqa: F401


def test_deprecation(monkeypatch):
    mpl.rcParams.update(mpl.rcParams.copy())  # Doesn't warn.

