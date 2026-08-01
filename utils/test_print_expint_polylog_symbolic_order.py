
def test_print_expint_polylog_symbolic_order():
    s, z = symbols("s, z")
    uresult = 'Liₛ(z)'
    aresult = 'polylog(s, z)'
    assert pretty(polylog(s, z)) == aresult
    assert upretty(polylog(s, z)) == uresult
    # TODO: TBD polylog(s - 1, z)
    uresult = 'Eₛ(z)'
    aresult = 'expint(s, z)'
    assert pretty(expint(s, z)) == aresult
    assert upretty(expint(s, z)) == uresult

