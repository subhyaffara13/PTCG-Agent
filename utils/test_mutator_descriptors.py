
def test_mutator_descriptors():
    zr = np.arange(30, dtype="float32").reshape(5, 6)  # row-major
    zc = zr.reshape(6, 5).transpose()  # column-major

    m.fixed_mutator_r(zr)
    m.fixed_mutator_c(zc)
    m.fixed_mutator_a(zr)
    m.fixed_mutator_a(zc)
    with pytest.raises(TypeError) as excinfo:
        m.fixed_mutator_r(zc)
    assert (
        "(arg0: numpy.ndarray[numpy.float32[5, 6],"
        " flags.writeable, flags.c_contiguous]) -> None" in str(excinfo.value)
    )
    with pytest.raises(TypeError) as excinfo:
        m.fixed_mutator_c(zr)
    assert (
        "(arg0: numpy.ndarray[numpy.float32[5, 6],"
        " flags.writeable, flags.f_contiguous]) -> None" in str(excinfo.value)
    )
    with pytest.raises(TypeError) as excinfo:
        m.fixed_mutator_a(np.array([[1, 2], [3, 4]], dtype="float32"))
    assert "(arg0: numpy.ndarray[numpy.float32[5, 6], flags.writeable]) -> None" in str(
        excinfo.value
    )
    zr.flags.writeable = False
    with pytest.raises(TypeError):
        m.fixed_mutator_r(zr)
    with pytest.raises(TypeError):
        m.fixed_mutator_a(zr)

