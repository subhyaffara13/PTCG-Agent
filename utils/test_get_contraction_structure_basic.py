
def test_get_contraction_structure_basic():
    x = IndexedBase('x')
    y = IndexedBase('y')
    i, j = Idx('i'), Idx('j')
    assert get_contraction_structure(x[i]*y[j]) == {None: {x[i]*y[j]}}
    assert get_contraction_structure(x[i] + y[j]) == {None: {x[i], y[j]}}
    assert get_contraction_structure(x[i]*y[i]) == {(i,): {x[i]*y[i]}}
    assert get_contraction_structure(
        1 + x[i]*y[i]) == {None: {S.One}, (i,): {x[i]*y[i]}}
    assert get_contraction_structure(x[i]**y[i]) == {None: {x[i]**y[i]}}

