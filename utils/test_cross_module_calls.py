
def test_cross_module_calls():
    import pybind11_cross_module_tests as cm

    v1 = m.LocalVec()
    v1.append(m.LocalType(1))
    v2 = cm.LocalVec()
    v2.append(cm.LocalType(2))

    # Returning the self pointer should get picked up as returning an existing
    # instance (even when that instance is of a foreign, non-local type).
    assert m.return_self(v1) is v1
    assert cm.return_self(v2) is v2
    assert m.return_self(v2) is v2
    assert cm.return_self(v1) is v1

    assert m.LocalVec is not cm.LocalVec
    # Returning a copy, on the other hand, always goes to the local type,
    # regardless of where the source type came from.
    assert type(m.return_copy(v1)) is m.LocalVec
    assert type(m.return_copy(v2)) is m.LocalVec
    assert type(cm.return_copy(v1)) is cm.LocalVec
    assert type(cm.return_copy(v2)) is cm.LocalVec

    # Test the example given in the documentation (which also tests inheritance casting):
    mycat = m.Cat("Fluffy")
    mydog = cm.Dog("Rover")
    assert mycat.get_name() == "Fluffy"
    assert mydog.name() == "Rover"
    assert m.Cat.__base__.__name__ == "Pet"
    assert cm.Dog.__base__.__name__ == "Pet"
    assert m.Cat.__base__ is not cm.Dog.__base__
    assert m.pet_name(mycat) == "Fluffy"
    assert m.pet_name(mydog) == "Rover"
    assert cm.pet_name(mycat) == "Fluffy"
    assert cm.pet_name(mydog) == "Rover"

    assert m.MixGL is not cm.MixGL
    a = m.MixGL(1)
    b = cm.MixGL(2)
    assert m.get_gl_value(a) == 11
    assert m.get_gl_value(b) == 12
    assert cm.get_gl_value(a) == 101
    assert cm.get_gl_value(b) == 102

    c, d = m.MixGL2(3), cm.MixGL2(4)
    with pytest.raises(TypeError) as excinfo:
        m.get_gl_value(c)
    assert "incompatible function arguments" in str(excinfo.value)
    with pytest.raises(TypeError) as excinfo:
        m.get_gl_value(d)
    assert "incompatible function arguments" in str(excinfo.value)

