
def test_local_dict_symbol_to_fcn():
    x = Symbol('x')
    d = {'foo': Function('bar')}
    assert parse_expr('foo(x)', local_dict=d) == d['foo'](x)
    d = {'foo': Symbol('baz')}
    raises(TypeError, lambda: parse_expr('foo(x)', local_dict=d))

