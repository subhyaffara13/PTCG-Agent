
def test_to_python():
    mat = m.Matrix(5, 4)
    assert memoryview(mat).shape == (5, 4)

    assert mat[2, 3] == 0
    mat[2, 3] = 4.0
    mat[3, 2] = 7.0
    assert mat[2, 3] == 4
    assert mat[3, 2] == 7
    assert struct.unpack_from("f", mat, (3 * 4 + 2) * 4) == (7,)
    assert struct.unpack_from("f", mat, (2 * 4 + 3) * 4) == (4,)

    mat2 = np.array(mat, copy=False)
    assert mat2.shape == (5, 4)
    assert abs(mat2).sum() == 11
    assert mat2[2, 3] == 4
    assert mat2[3, 2] == 7
    mat2[2, 3] = 5
    assert mat2[2, 3] == 5

    cstats = ConstructorStats.get(m.Matrix)
    assert cstats.alive() == 1
    del mat
    pytest.gc_collect()
    assert cstats.alive() == 1
    del mat2  # holds a mat reference
    pytest.gc_collect()
    assert cstats.alive() == 0
    assert cstats.values() == ["5x4 matrix"]
    assert cstats.copy_constructions == 0
    # assert cstats.move_constructions >= 0  # Don't invoke any
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0

