
def test_large_string_coercion_error(str_dt):
    very_large = np.iinfo(np.intc).max // np.dtype(f"{str_dt}1").itemsize
    try:
        large_string = "A" * (very_large + 1)
    except Exception:
        # We may not be able to create this Python string on 32bit.
        pytest.skip("python failed to create huge string")

    class MyStr:
        def __str__(self):
            return large_string

    try:
        # TypeError from NumPy, or OverflowError from 32bit Python.
        with pytest.raises((TypeError, OverflowError)):
            np.array([large_string], dtype=str_dt)

        # Same as above, but input has to be converted to a string.
        with pytest.raises((TypeError, OverflowError)):
            np.array([MyStr()], dtype=str_dt)
    except MemoryError:
        # Catch memory errors, because `requires_memory` would do so.
        raise AssertionError("Ops should raise before any large allocation.")

