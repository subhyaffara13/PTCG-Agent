
def test_singular_values():
    x = Symbol('x', real=True)

    A = Matrix([[0, 1*I], [2, 0]])
    # if singular values can be sorted, they should be in decreasing order
    assert A.singular_values() == [2, 1]

    A = eye(3)
    A[1, 1] = x
    A[2, 2] = 5
    vals = A.singular_values()
    # since Abs(x) cannot be sorted, test set equality
    assert set(vals) == {5, 1, Abs(x)}

    A = Matrix([[sin(x), cos(x)], [-cos(x), sin(x)]])
    vals = [sv.trigsimp() for sv in A.singular_values()]
    assert vals == [S.One, S.One]

    A = Matrix([
        [2, 4],
        [1, 3],
        [0, 0],
        [0, 0]
        ])
    assert A.singular_values() == \
        [sqrt(sqrt(221) + 15), sqrt(15 - sqrt(221))]
    assert A.T.singular_values() == \
        [sqrt(sqrt(221) + 15), sqrt(15 - sqrt(221)), 0, 0]

