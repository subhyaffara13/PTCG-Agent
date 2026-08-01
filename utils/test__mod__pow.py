
def test_Mod_Pow():
    # modular exponentiation
    assert isinstance(Mod(Pow(2, 2, evaluate=False), 3), Integer)

    assert Mod(Pow(4, 13, evaluate=False), 497) == Mod(Pow(4, 13), 497)
    assert Mod(Pow(2, 10000000000, evaluate=False), 3) == 1
    assert Mod(Pow(32131231232, 9**10**6, evaluate=False),10**12) == \
        pow(32131231232,9**10**6,10**12)
    assert Mod(Pow(33284959323, 123**999, evaluate=False),11**13) == \
        pow(33284959323,123**999,11**13)
    assert Mod(Pow(78789849597, 333**555, evaluate=False),12**9) == \
        pow(78789849597,333**555,12**9)

    # modular nested exponentiation
    expr = Pow(2, 2, evaluate=False)
    expr = Pow(2, expr, evaluate=False)
    assert Mod(expr, 3**10) == 16
    expr = Pow(2, expr, evaluate=False)
    assert Mod(expr, 3**10) == 6487
    expr = Pow(2, expr, evaluate=False)
    assert Mod(expr, 3**10) == 32191
    expr = Pow(2, expr, evaluate=False)
    assert Mod(expr, 3**10) == 18016
    expr = Pow(2, expr, evaluate=False)
    assert Mod(expr, 3**10) == 5137

    expr = Pow(2, 2, evaluate=False)
    expr = Pow(expr, 2, evaluate=False)
    assert Mod(expr, 3**10) == 16
    expr = Pow(expr, 2, evaluate=False)
    assert Mod(expr, 3**10) == 256
    expr = Pow(expr, 2, evaluate=False)
    assert Mod(expr, 3**10) == 6487
    expr = Pow(expr, 2, evaluate=False)
    assert Mod(expr, 3**10) == 38281
    expr = Pow(expr, 2, evaluate=False)
    assert Mod(expr, 3**10) == 15928

    expr = Pow(2, 2, evaluate=False)
    expr = Pow(expr, expr, evaluate=False)
    assert Mod(expr, 3**10) == 256
    expr = Pow(expr, expr, evaluate=False)
    assert Mod(expr, 3**10) == 9229
    expr = Pow(expr, expr, evaluate=False)
    assert Mod(expr, 3**10) == 25708
    expr = Pow(expr, expr, evaluate=False)
    assert Mod(expr, 3**10) == 26608
    expr = Pow(expr, expr, evaluate=False)
    # XXX This used to fail in a nondeterministic way because of overflow
    # error.
    assert Mod(expr, 3**10) == 1966

