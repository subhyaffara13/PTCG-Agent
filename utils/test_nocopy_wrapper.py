
def test_nocopy_wrapper():
    # get_elem requires a column-contiguous matrix reference, but should be
    # callable with other types of matrix (via copying):
    int_matrix_colmajor = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], order="F")
    dbl_matrix_colmajor = np.array(
        int_matrix_colmajor, dtype="double", order="F", copy=True
    )
    int_matrix_rowmajor = np.array(int_matrix_colmajor, order="C", copy=True)
    dbl_matrix_rowmajor = np.array(
        int_matrix_rowmajor, dtype="double", order="C", copy=True
    )

    # All should be callable via get_elem:
    assert m.get_elem(int_matrix_colmajor) == 8
    assert m.get_elem(dbl_matrix_colmajor) == 8
    assert m.get_elem(int_matrix_rowmajor) == 8
    assert m.get_elem(dbl_matrix_rowmajor) == 8

    # All but the second should fail with m.get_elem_nocopy:
    with pytest.raises(TypeError) as excinfo:
        m.get_elem_nocopy(int_matrix_colmajor)
    assert "get_elem_nocopy(): incompatible function arguments." in str(excinfo.value)
    assert ", flags.f_contiguous" in str(excinfo.value)
    assert m.get_elem_nocopy(dbl_matrix_colmajor) == 8
    with pytest.raises(TypeError) as excinfo:
        m.get_elem_nocopy(int_matrix_rowmajor)
    assert "get_elem_nocopy(): incompatible function arguments." in str(excinfo.value)
    assert ", flags.f_contiguous" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.get_elem_nocopy(dbl_matrix_rowmajor)
    assert "get_elem_nocopy(): incompatible function arguments." in str(excinfo.value)
    assert ", flags.f_contiguous" in str(excinfo.value)

    # For the row-major test, we take a long matrix in row-major, so only the third is allowed:
    with pytest.raises(TypeError) as excinfo:
        m.get_elem_rm_nocopy(int_matrix_colmajor)
    assert "get_elem_rm_nocopy(): incompatible function arguments." in str(
        excinfo.value
    )
    assert ", flags.c_contiguous" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.get_elem_rm_nocopy(dbl_matrix_colmajor)
    assert "get_elem_rm_nocopy(): incompatible function arguments." in str(
        excinfo.value
    )
    assert ", flags.c_contiguous" in str(excinfo.value)
    assert m.get_elem_rm_nocopy(int_matrix_rowmajor) == 8
    with pytest.raises(TypeError) as excinfo:
        m.get_elem_rm_nocopy(dbl_matrix_rowmajor)
    assert "get_elem_rm_nocopy(): incompatible function arguments." in str(
        excinfo.value
    )
    assert ", flags.c_contiguous" in str(excinfo.value)

