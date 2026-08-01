
def test_large_string_addition_error(str_dt):
    very_large = np.iinfo(np.intc).max // np.dtype(f"{str_dt}1").itemsize

    a = np.array(["A" * very_large], dtype=str_dt)
    b = np.array("B", dtype=str_dt)
    try:
        with pytest.raises(TypeError):
            np.add(a, b)
        with pytest.raises(TypeError):
            np.add(a, a)
    except MemoryError:
        # Catch memory errors, because `requires_memory` would do so.
        raise AssertionError("Ops should raise before any large allocation.")

