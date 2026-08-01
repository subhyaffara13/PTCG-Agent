
def test_contraction_structure_simple_Pow():
    x = IndexedBase('x')
    y = IndexedBase('y')
    i, j, k = Idx('i'), Idx('j'), Idx('k')
    ii_jj = x[i, i]**y[j, j]
    assert get_contraction_structure(ii_jj) == {
        None: {ii_jj},
        ii_jj: [
            {(i,): {x[i, i]}},
            {(j,): {y[j, j]}}
        ]
    }

    ii_jk = x[i, i]**y[j, k]
    assert get_contraction_structure(ii_jk) == {
        None: {x[i, i]**y[j, k]},
        x[i, i]**y[j, k]: [
            {(i,): {x[i, i]}}
        ]
    }

