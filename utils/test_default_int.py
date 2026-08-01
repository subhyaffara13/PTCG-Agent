
def test_default_int(install_temp):
    import checks

    assert checks.get_default_integer() is np.dtype(int)

