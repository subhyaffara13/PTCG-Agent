
def test_pcolormesh_underflow_error():
    """
    Test that underflow errors don't crop up in pcolormesh.  Probably
    a numpy bug (https://github.com/numpy/numpy/issues/25810).
    """
    with np.errstate(under="raise"):
        x = np.arange(0, 3, 0.1)
        y = np.arange(0, 6, 0.1)
        z = np.random.randn(len(y), len(x))
        fig, ax = plt.subplots()
        ax.pcolormesh(x, y, z)

