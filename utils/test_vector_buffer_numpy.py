
def test_vector_buffer_numpy():
    np = pytest.importorskip("numpy")
    a = np.array([1, 2, 3, 4], dtype=np.int32)
    with pytest.raises(TypeError):
        m.VectorInt(a)

    a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], dtype=np.uintc)
    v = m.VectorInt(a[0, :])
    assert len(v) == 4
    assert v[2] == 3
    ma = np.asarray(v)
    ma[2] = 5
    assert v[2] == 5

    v = m.VectorInt(a[:, 1])
    assert len(v) == 3
    assert v[2] == 10

    v = m.get_vectorstruct()
    assert v[0].x == 5
    ma = np.asarray(v)
    ma[1]["x"] = 99
    assert v[1].x == 99

    v = m.VectorStruct(
        np.zeros(
            3,
            dtype=np.dtype(
                [("w", "bool"), ("x", "I"), ("y", "float64"), ("z", "bool")], align=True
            ),
        )
    )
    assert len(v) == 3

    b = np.array([1, 2, 3, 4], dtype=np.uint8)
    v = m.VectorUChar(b[::2])
    assert v[1] == 3

