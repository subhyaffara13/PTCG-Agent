
def test_Dimension_functions():
    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(cos(length)))
    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(acos(angle)))
    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(atan2(length, time)))
    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(log(length)))
    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(log(100, length)))
    raises(TypeError, lambda: dimsys_SI.get_dimensional_dependencies(log(length, 10)))

    assert dimsys_SI.get_dimensional_dependencies(pi) == {}

    assert dimsys_SI.get_dimensional_dependencies(cos(1)) == {}
    assert dimsys_SI.get_dimensional_dependencies(cos(angle)) == {}

    assert dimsys_SI.get_dimensional_dependencies(atan2(length, length)) == {}

    assert dimsys_SI.get_dimensional_dependencies(log(length / length, length / length)) == {}

    assert dimsys_SI.get_dimensional_dependencies(Abs(length)) == {length: 1}
    assert dimsys_SI.get_dimensional_dependencies(Abs(length / length)) == {}

    assert dimsys_SI.get_dimensional_dependencies(sqrt(-1)) == {}

