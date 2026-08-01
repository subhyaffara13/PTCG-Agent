
def test_scoped_enum():
    assert m.test_scoped_enum(m.ScopedEnum.Three) == "ScopedEnum::Three"
    z = m.ScopedEnum.Two
    assert m.test_scoped_enum(z) == "ScopedEnum::Two"

    # Scoped enums will *NOT* accept ==/!= int comparisons (Will always return False)
    assert not z == 3
    assert not 3 == z
    assert z != 3
    assert 3 != z
    # Compare with None
    assert z != None  # noqa: E711
    assert not (z == None)  # noqa: E711
    # Compare with an object
    assert z != object()
    assert not (z == object())
    # Scoped enums will *NOT* accept >, <, >= and <= int comparisons (Will throw exceptions)
    with pytest.raises(TypeError):
        z > 3  # noqa: B015
    with pytest.raises(TypeError):
        z < 3  # noqa: B015
    with pytest.raises(TypeError):
        z >= 3  # noqa: B015
    with pytest.raises(TypeError):
        z <= 3  # noqa: B015

    # order
    assert m.ScopedEnum.Two < m.ScopedEnum.Three
    assert m.ScopedEnum.Three > m.ScopedEnum.Two
    assert m.ScopedEnum.Two <= m.ScopedEnum.Three
    assert m.ScopedEnum.Two <= m.ScopedEnum.Two
    assert m.ScopedEnum.Two >= m.ScopedEnum.Two
    assert m.ScopedEnum.Three >= m.ScopedEnum.Two

