
def test_return_vector_bool_raw_ptr():
    # Add `while True:` for manual leak checking.
    v = m.return_vector_bool_raw_ptr()
    assert isinstance(v, list)
    assert len(v) == 4513

