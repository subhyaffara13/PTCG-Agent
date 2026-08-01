
def test_function_record_leaks():
    class RaisingRepr:
        def __repr__(self):
            raise RuntimeError("Surprise!")

    with pytest.raises(RuntimeError):
        m.register_large_capture_with_invalid_arguments(m)
    with pytest.raises(RuntimeError):
        m.register_with_raising_repr(m, RaisingRepr())

