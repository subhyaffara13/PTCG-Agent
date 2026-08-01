
def test_unscoped_enum():
    assert str(m.UnscopedEnum.EOne) == "UnscopedEnum.EOne"
    assert str(m.UnscopedEnum.ETwo) == "UnscopedEnum.ETwo"
    assert str(m.EOne) == "UnscopedEnum.EOne"
    assert repr(m.UnscopedEnum.EOne) == "<UnscopedEnum.EOne: 1>"
    assert repr(m.UnscopedEnum.ETwo) == "<UnscopedEnum.ETwo: 2>"
    assert repr(m.EOne) == "<UnscopedEnum.EOne: 1>"

    # name property
    assert m.UnscopedEnum.EOne.name == "EOne"
    assert m.UnscopedEnum.EOne.value == 1
    assert m.UnscopedEnum.ETwo.name == "ETwo"
    assert m.UnscopedEnum.ETwo.value == 2
    assert m.EOne is m.UnscopedEnum.EOne
    # name, value readonly
    with pytest.raises(AttributeError):
        m.UnscopedEnum.EOne.name = ""
    with pytest.raises(AttributeError):
        m.UnscopedEnum.EOne.value = 10
    # name, value returns a copy
    # TODO: Neither the name nor value tests actually check against aliasing.
    # Use a mutable type that has reference semantics.
    nonaliased_name = m.UnscopedEnum.EOne.name
    nonaliased_name = "bar"  # noqa: F841
    assert m.UnscopedEnum.EOne.name == "EOne"
    nonaliased_value = m.UnscopedEnum.EOne.value
    nonaliased_value = 10  # noqa: F841
    assert m.UnscopedEnum.EOne.value == 1

    # __members__ property
    assert m.UnscopedEnum.__members__ == {
        "EOne": m.UnscopedEnum.EOne,
        "ETwo": m.UnscopedEnum.ETwo,
        "EThree": m.UnscopedEnum.EThree,
    }
    # __members__ readonly
    with pytest.raises(AttributeError):
        m.UnscopedEnum.__members__ = {}
    # __members__ returns a copy
    nonaliased_members = m.UnscopedEnum.__members__
    nonaliased_members["bar"] = "baz"
    assert m.UnscopedEnum.__members__ == {
        "EOne": m.UnscopedEnum.EOne,
        "ETwo": m.UnscopedEnum.ETwo,
        "EThree": m.UnscopedEnum.EThree,
    }

    for docstring_line in """An unscoped enumeration

Members:

  EOne : Docstring for EOne

  ETwo : Docstring for ETwo

  EThree : Docstring for EThree""".split(
        "\n"
    ):
        assert docstring_line in m.UnscopedEnum.__doc__

    # Unscoped enums will accept ==/!= int comparisons
    y = m.UnscopedEnum.ETwo
    assert y == 2
    assert 2 == y
    assert y != 3
    assert 3 != y
    # Compare with None
    assert y != None  # noqa: E711
    assert not (y == None)  # noqa: E711
    # Compare with an object
    assert y != object()
    assert not (y == object())
    # Compare with string
    assert y != "2"
    assert "2" != y
    assert not ("2" == y)
    assert not (y == "2")

    with pytest.raises(TypeError):
        y < object()  # noqa: B015

    with pytest.raises(TypeError):
        y <= object()  # noqa: B015

    with pytest.raises(TypeError):
        y > object()  # noqa: B015

    with pytest.raises(TypeError):
        y >= object()  # noqa: B015

    with pytest.raises(TypeError):
        y | object()

    with pytest.raises(TypeError):
        y & object()

    with pytest.raises(TypeError):
        y ^ object()

    assert int(m.UnscopedEnum.ETwo) == 2
    assert str(m.UnscopedEnum(2)) == "UnscopedEnum.ETwo"

    # order
    assert m.UnscopedEnum.EOne < m.UnscopedEnum.ETwo
    assert m.UnscopedEnum.EOne < 2
    assert m.UnscopedEnum.ETwo > m.UnscopedEnum.EOne
    assert m.UnscopedEnum.ETwo > 1
    assert m.UnscopedEnum.ETwo <= 2
    assert m.UnscopedEnum.ETwo >= 2
    assert m.UnscopedEnum.EOne <= m.UnscopedEnum.ETwo
    assert m.UnscopedEnum.EOne <= 2
    assert m.UnscopedEnum.ETwo >= m.UnscopedEnum.EOne
    assert m.UnscopedEnum.ETwo >= 1
    assert not (m.UnscopedEnum.ETwo < m.UnscopedEnum.EOne)
    assert not (2 < m.UnscopedEnum.EOne)

    # arithmetic
    assert m.UnscopedEnum.EOne & m.UnscopedEnum.EThree == m.UnscopedEnum.EOne
    assert m.UnscopedEnum.EOne | m.UnscopedEnum.ETwo == m.UnscopedEnum.EThree
    assert m.UnscopedEnum.EOne ^ m.UnscopedEnum.EThree == m.UnscopedEnum.ETwo

