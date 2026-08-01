
def test_issue9474():
    mods = [None, 'math']
    if numpy:
        mods.append('numpy')
    if mpmath:
        mods.append('mpmath')
    for mod in mods:
        f = lambdify(x, S.One/x, modules=mod)
        assert f(2) == 0.5
        f = lambdify(x, floor(S.One/x), modules=mod)
        assert f(2) == 0

    for absfunc, modules in product([Abs, abs], mods):
        f = lambdify(x, absfunc(x), modules=modules)
        assert f(-1) == 1
        assert f(1) == 1
        assert f(3+4j) == 5

