
def test_dict_list():

    A = ReferenceFrame('A')
    B = ReferenceFrame('B')
    C = ReferenceFrame('C')
    D = ReferenceFrame('D')
    E = ReferenceFrame('E')
    F = ReferenceFrame('F')

    B.orient_axis(A, A.x, 1.0)
    C.orient_axis(B, B.x, 1.0)
    D.orient_axis(C, C.x, 1.0)

    assert D._dict_list(A, 0) == [D, C, B, A]

    E.orient_axis(D, D.x, 1.0)

    assert C._dict_list(A, 0) == [C, B, A]
    assert C._dict_list(E, 0) == [C, D, E]

    # only 0, 1, 2 permitted for second argument
    raises(ValueError, lambda: C._dict_list(E, 5))
    # no connecting path
    raises(ValueError, lambda: F._dict_list(A, 0))

