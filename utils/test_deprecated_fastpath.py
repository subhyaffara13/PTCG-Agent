
def test_deprecated_fastpath():
    msg = "[Uu]nexpected keyword argument"
    with pytest.raises(TypeError, match=msg):
        Index(np.array(["a", "b"], dtype=object), name="test", fastpath=True)

    with pytest.raises(TypeError, match=msg):
        Index(np.array([1, 2, 3], dtype="int64"), name="test", fastpath=True)

    with pytest.raises(TypeError, match=msg):
        RangeIndex(0, 5, 2, name="test", fastpath=True)

    with pytest.raises(TypeError, match=msg):
        CategoricalIndex(["a", "b", "c"], name="test", fastpath=True)

