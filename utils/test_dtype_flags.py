
def test_dtype_flags(install_temp):
    import checks
    dtype = np.dtype("i,O")  # dtype with somewhat interesting flags
    assert dtype.flags == checks.get_dtype_flags(dtype)

