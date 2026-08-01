
def test_var_keywords():
    ns = {"var": var}
    eval("var('x y', real=True)", ns)
    assert ns['x'].is_real and ns['y'].is_real

