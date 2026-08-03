import copy

def test_flatten():
    assert flatten((1, (1,))) == [1, 1]
    assert flatten((x, (x,))) == [x, x]

    ls = [[(-2, -1), (1, 2)], [(0, 0)]]

    assert flatten(ls, levels=0) == ls
    assert flatten(ls, levels=1) == [(-2, -1), (1, 2), (0, 0)]
    assert flatten(ls, levels=2) == [-2, -1, 1, 2, 0, 0]
    assert flatten(ls, levels=3) == [-2, -1, 1, 2, 0, 0]

    raises(ValueError, lambda: flatten(ls, levels=-1))

    class MyOp(Basic):
        pass

    assert flatten([MyOp(x, y), z]) == [MyOp(x, y), z]
    assert flatten([MyOp(x, y), z], cls=MyOp) == [x, y, z]

    assert flatten({1, 11, 2}) == list({1, 11, 2})


def test_flatten():
    from sympy.matrices.dense import Matrix
    for ArrayType in [ImmutableDenseNDimArray, ImmutableSparseNDimArray, Matrix]:
        A = ArrayType(range(24)).reshape(4, 6)
        assert list(Flatten(A)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

        for i, v in enumerate(Flatten(A)):
            assert i == v


def test_flatten():
    assert flatten(Basic(S(1), S(2), Basic(S(3), S(4)))) == \
        Basic(S(1), S(2), S(3), S(4))


def test_flatten():
    """Tests whether there is basic denesting functionality"""
    inner = ConditionSet(x, sin(x) + x > 0)
    outer = ConditionSet(x, Contains(x, inner), S.Reals)
    assert outer == ConditionSet(x, sin(x) + x > 0, S.Reals)

    inner = ConditionSet(y, sin(y) + y > 0)
    outer = ConditionSet(x, Contains(y, inner), S.Reals)
    assert outer != ConditionSet(x, sin(x) + x > 0, S.Reals)

    inner = ConditionSet(x, sin(x) + x > 0).intersect(Interval(-1, 1))
    outer = ConditionSet(x, Contains(x, inner), S.Reals)
    assert outer == ConditionSet(x, sin(x) + x > 0, Interval(-1, 1))


def test_flatten(nested, result):
    if result is None:
        val = flatten(nested, result)
        assert len(val) == 20
    else:
        _result = copy(result)  # because pytest passes parameters as is
        nexisting = len(_result)
        val = flatten(nested, _result)
        assert len(val) == len(_result) == 20 + nexisting

    assert issubclass(type(val), tuple)

