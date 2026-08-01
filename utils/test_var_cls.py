
def test_var_cls():
    ns = {"var": var, "Function": Function}
    eval("var('f', cls=Function)", ns)

    assert isinstance(ns['f'], FunctionClass)

    eval("var('g,h', cls=Function)", ns)

    assert isinstance(ns['g'], FunctionClass)
    assert isinstance(ns['h'], FunctionClass)

