
def test_cpp_casting():
    assert m.cpp_copy(m.fixed_r()) == 22.0
    assert m.cpp_copy(m.fixed_c()) == 22.0
    z = np.array([[5.0, 6], [7, 8]])
    assert m.cpp_copy(z) == 7.0
    assert m.cpp_copy(m.get_cm_ref()) == 21.0
    assert m.cpp_copy(m.get_rm_ref()) == 21.0
    assert m.cpp_ref_c(m.get_cm_ref()) == 21.0
    assert m.cpp_ref_r(m.get_rm_ref()) == 21.0
    with pytest.raises(RuntimeError) as excinfo:
        # Can't reference m.fixed_c: it contains floats, m.cpp_ref_any wants doubles
        m.cpp_ref_any(m.fixed_c())
    assert "Unable to cast Python instance" in str(excinfo.value)
    with pytest.raises(RuntimeError) as excinfo:
        # Can't reference m.fixed_r: it contains floats, m.cpp_ref_any wants doubles
        m.cpp_ref_any(m.fixed_r())
    assert "Unable to cast Python instance" in str(excinfo.value)
    assert m.cpp_ref_any(m.ReturnTester.create()) == 1.0

    assert m.cpp_ref_any(m.get_cm_ref()) == 21.0
    assert m.cpp_ref_any(m.get_cm_ref()) == 21.0

