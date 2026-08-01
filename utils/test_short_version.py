
def test_short_version():
    # Check numpy.short_version actually exists
    if np.version.release:
        assert_(np.__version__ == np.version.short_version,
                "short_version mismatch in release version")
    else:
        assert_(np.__version__.split("+")[0] == np.version.short_version,
                "short_version mismatch in development version")

