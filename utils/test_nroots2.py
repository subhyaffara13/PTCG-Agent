
def test_nroots2():
    p = Poly(x**5 + 3*x + 1, x)

    roots = p.nroots(n=3)
    # The order of roots matters. The roots are ordered by their real
    # components (if they agree, then by their imaginary components),
    # with real roots appearing first.
    assert [str(r) for r in roots] == \
            ['-0.332', '-0.839 - 0.944*I', '-0.839 + 0.944*I',
                '1.01 - 0.937*I', '1.01 + 0.937*I']

    roots = p.nroots(n=5)
    assert [str(r) for r in roots] == \
            ['-0.33199', '-0.83907 - 0.94385*I', '-0.83907 + 0.94385*I',
              '1.0051 - 0.93726*I', '1.0051 + 0.93726*I']

