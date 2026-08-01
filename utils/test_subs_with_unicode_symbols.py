
def test_subs_with_unicode_symbols():
    expr = Symbol('var1')
    replaced = expr.subs('var1', 'x')
    assert replaced.name == 'x'

    replaced = expr.subs('var1', 'x')
    assert replaced.name == 'x'

