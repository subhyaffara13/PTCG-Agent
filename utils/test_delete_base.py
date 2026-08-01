
def test_delete_base(idx):
    expected = idx[1:]
    result = idx.delete(0)
    assert result.equals(expected)
    assert result.name == expected.name

    expected = idx[:-1]
    result = idx.delete(-1)
    assert result.equals(expected)
    assert result.name == expected.name

    msg = "index 6 is out of bounds for axis 0 with size 6"
    with pytest.raises(IndexError, match=msg):
        idx.delete(len(idx))

