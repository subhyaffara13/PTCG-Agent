
def test_string_size_dtype_large_repr(str_dt):
    size = np.iinfo(np.intc).max // np.dtype(f"{str_dt}1").itemsize
    size_str = str(size)

    dtype = np.dtype((str_dt, size))
    assert size_str in dtype.str
    assert size_str in str(dtype)
    assert size_str in repr(dtype)

