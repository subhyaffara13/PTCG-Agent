
def test_EmptySequence():
    assert S.EmptySequence is EmptySequence

    assert S.EmptySequence.interval is S.EmptySet
    assert S.EmptySequence.length is S.Zero

    assert list(S.EmptySequence) == []

