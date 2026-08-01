
def test_Dimension_definition():
    assert dimsys_SI.get_dimensional_dependencies(length) == {length: 1}
    assert length.name == Symbol("length")
    assert length.symbol == Symbol("L")

    halflength = sqrt(length)
    assert dimsys_SI.get_dimensional_dependencies(halflength) == {length: S.Half}

