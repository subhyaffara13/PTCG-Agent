
def test_vector_buffer():
    b = bytearray([1, 2, 3, 4])
    v = m.VectorUChar(b)
    assert v[1] == 2
    v[2] = 5
    mv = memoryview(v)  # We expose the buffer interface
    assert mv[2] == 5
    mv[2] = 6
    assert v[2] == 6

    mv = memoryview(b)
    v = m.VectorUChar(mv[::2])
    assert v[1] == 3

    with pytest.raises(RuntimeError) as excinfo:
        m.create_undeclstruct()  # Undeclared struct contents, no buffer interface
    assert "NumPy type info missing for " in str(excinfo.value)

