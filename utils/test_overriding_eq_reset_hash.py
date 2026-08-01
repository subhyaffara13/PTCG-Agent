
def test_overriding_eq_reset_hash():
    assert m.Comparable(15) is not m.Comparable(15)
    assert m.Comparable(15) == m.Comparable(15)

    with pytest.raises(TypeError) as excinfo:
        hash(m.Comparable(15))
    assert str(excinfo.value).startswith("unhashable type:")

    for hashable in (m.Hashable, m.Hashable2):
        assert hashable(15) is not hashable(15)
        assert hashable(15) == hashable(15)

        assert hash(hashable(15)) == 15
        assert hash(hashable(15)) == hash(hashable(15))

