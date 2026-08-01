
def test_sho_sums():
    e1 = Sum(SHOKet(p)*SHOBra(p), (p, 0, 1))
    assert e1.doit() == SHOKet(0)*SHOBra(0) + SHOKet(1)*SHOBra(1)

    # Test qapply with Sum on the left
    assert qapply(
        Sum(SHOKet(p)*SHOBra(p), (p, 0, oo))*SHOKet(q),
        sum_doit=True
    ) == SHOKet(q)

    # Test qapply with Sum on the right
    a = IndexedBase('a')
    n = symbols('n', cls=Idx)
    result = qapply(SHOBra(q)*Sum(a[n]*SHOKet(n), (n,0,oo)), sum_doit=True)
    assert result == a[q]

    # Test qapply with a product of Sums
    result = qapply(
        SHOBra(q)*Sum(SHOKet(p)*SHOBra(p), (p, 0, oo))*Sum(a[n]*SHOKet(n), (n,0,oo)),
        sum_doit=True
    )
    assert result == a[q]

    with raises(ValueError):
        result = qapply(
            SHOBra(q)*Sum(SHOKet(p)*SHOBra(p), (p, 0, oo))*Sum(a[p]*SHOKet(p), (p,0,oo)),
            sum_doit=True
        )

