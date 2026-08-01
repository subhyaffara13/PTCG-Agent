
def test_contraction_structure_Pow_in_Pow():
    x = IndexedBase('x')
    y = IndexedBase('y')
    z = IndexedBase('z')
    i, j, k = Idx('i'), Idx('j'), Idx('k')
    ii_jj_kk = x[i, i]**y[j, j]**z[k, k]
    expected = {
        None: {ii_jj_kk},
        ii_jj_kk: [
            {(i,): {x[i, i]}},
            {
                None: {y[j, j]**z[k, k]},
                y[j, j]**z[k, k]: [
                    {(j,): {y[j, j]}},
                    {(k,): {z[k, k]}}
                ]
            }
        ]
    }
    assert get_contraction_structure(ii_jj_kk) == expected

