
def test_issue_14565():
    # removed redundancy
    assert dumeq(nonlinsolve([k + m, k + m*exp(-2*pi*k)], [k, m]) ,
        FiniteSet((-n*I, ImageSet(Lambda(n, n*I), S.Integers))))

