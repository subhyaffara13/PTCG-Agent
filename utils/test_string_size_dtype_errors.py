
def test_string_size_dtype_errors(str_dt, size):
    if size > 0:
        size = size // np.dtype(f"{str_dt}1").itemsize + 1

    with pytest.raises(ValueError):
        np.dtype((str_dt, size))
    with pytest.raises(TypeError):
        np.dtype(f"{str_dt}{size}")

