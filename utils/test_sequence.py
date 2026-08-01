
def test_sequence():
    cstats = ConstructorStats.get(m.Sequence)

    s = m.Sequence(5)
    assert cstats.values() == ["of size", "5"]

    assert "Sequence" in repr(s)
    assert len(s) == 5
    assert s[0] == 0
    assert s[3] == 0
    assert 12.34 not in s
    s[0], s[3] = 12.34, 56.78
    assert 12.34 in s
    assert s[0] == approx(12.34, rel=1e-05)
    assert s[3] == approx(56.78, rel=1e-05)

    rev = reversed(s)
    assert cstats.values() == ["of size", "5"]

    rev2 = s[::-1]
    assert cstats.values() == ["of size", "5"]

    it = iter(m.Sequence(0))
    for _ in range(3):  # __next__ must continue to raise StopIteration
        with pytest.raises(StopIteration):
            next(it)
    assert cstats.values() == ["of size", "0"]

    expected = [0, 56.78, 0, 0, 12.34]
    assert rev == approx(expected, rel=1e-05)
    assert rev2 == approx(expected, rel=1e-05)
    assert rev == rev2

    rev[0::2] = m.Sequence([2.0, 2.0, 2.0])
    assert cstats.values() == ["of size", "3", "from std::vector"]

    assert rev == approx([2, 56.78, 2, 0, 2], rel=1e-05)

    assert cstats.alive() == 4
    del it
    assert cstats.alive() == 3
    del s
    assert cstats.alive() == 2
    del rev
    assert cstats.alive() == 1
    del rev2
    assert cstats.alive() == 0

    assert cstats.values() == []
    assert cstats.default_constructions == 0
    assert cstats.copy_constructions == 0
    assert cstats.move_constructions >= 1
    assert cstats.copy_assignments == 0
    assert cstats.move_assignments == 0


def test_sequence(value: t.Any) -> bool:
    """Return true if the variable is a sequence. Sequences are variables
    that are iterable.
    """
    try:
        len(value)
        value.__getitem__  # noqa B018
    except Exception:
        return False

    return True


def test_sequence():
    form = SeqFormula(n**2, (n, 0, 5))
    per = SeqPer((1, 2, 3), (n, 0, 5))
    inter = SeqFormula(n**2)

    assert sequence(n**2, (n, 0, 5)) == form
    assert sequence((1, 2, 3), (n, 0, 5)) == per
    assert sequence(n**2) == inter

