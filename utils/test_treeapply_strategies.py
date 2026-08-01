
def test_treeapply_strategies():
    from sympy.strategies import chain, minimize
    join = {list: chain, tuple: minimize}

    assert treeapply(inc, join) == inc
    assert treeapply((inc, dec), join)(5) == minimize(inc, dec)(5)
    assert treeapply([inc, dec], join)(5) == chain(inc, dec)(5)
    tree = (inc, [dec, double])  # either inc or dec-then-double
    assert treeapply(tree, join)(5) == 6
    assert treeapply(tree, join)(1) == 0

    maximize = partial(minimize, objective=lambda x: -x)
    join = {list: chain, tuple: maximize}
    fn = treeapply(tree, join)
    assert fn(4) == 6  # highest value comes from the dec then double
    assert fn(1) == 2  # highest value comes from the inc

