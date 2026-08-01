
def test_union_dtypes(left, right, expected, names):
    left = pandas_dtype(left)
    right = pandas_dtype(right)
    a = Index([], dtype=left, name=names[0])
    b = Index([], dtype=right, name=names[1])
    result = a.union(b)
    assert result.dtype == expected
    assert result.name == names[2]

    # Testing name retention
    # TODO: pin down desired dtype; do we want it to be commutative?
    result = a.intersection(b)
    assert result.name == names[2]

