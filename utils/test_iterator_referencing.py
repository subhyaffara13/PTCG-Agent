
def test_iterator_referencing():
    """Test that iterators reference rather than copy their referents."""
    vec = m.VectorNonCopyableInt()
    vec.append(3)
    vec.append(5)
    assert [int(x) for x in vec] == [3, 5]
    # Increment everything to make sure the referents can be mutated
    for x in vec:
        x.set(int(x) + 1)
    assert [int(x) for x in vec] == [4, 6]

    vec = m.VectorNonCopyableIntPair()
    vec.append([3, 4])
    vec.append([5, 7])
    assert [int(x) for x in vec.keys()] == [3, 5]
    assert [int(x) for x in vec.values()] == [4, 7]
    for x in vec.keys():
        x.set(int(x) + 1)
    for x in vec.values():
        x.set(int(x) + 10)
    assert [int(x) for x in vec.keys()] == [4, 6]
    assert [int(x) for x in vec.values()] == [14, 17]

