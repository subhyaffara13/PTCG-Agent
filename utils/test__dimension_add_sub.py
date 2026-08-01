
def test_Dimension_add_sub():
    assert length + length == length
    assert length - length == length
    assert -length == length

    raises(TypeError, lambda: length + foot)
    raises(TypeError, lambda: foot + length)
    raises(TypeError, lambda: length - foot)
    raises(TypeError, lambda: foot - length)

    # issue 14547 - only raise error for dimensional args; allow
    # others to pass
    x = Symbol('x')
    e = length + x
    assert e == x + length and e.is_Add and set(e.args) == {length, x}
    e = length + 1
    assert e == 1 + length == 1 - length and e.is_Add and set(e.args) == {length, 1}

    assert dimsys_SI.get_dimensional_dependencies(mass * length / time**2 + force) == \
            {length: 1, mass: 1, time: -2}
    assert dimsys_SI.get_dimensional_dependencies(mass * length / time**2 + force -
                                                   pressure * length**2) == \
            {length: 1, mass: 1, time: -2}

    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(mass * length / time**2 + pressure))

