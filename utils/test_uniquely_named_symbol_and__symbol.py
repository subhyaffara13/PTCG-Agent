
def test_uniquely_named_symbol_and_Symbol():
    F = uniquely_named_symbol
    x = Symbol('x')
    assert F(x) == x
    assert F('x') == x
    assert str(F('x', x)) == 'x0'
    assert str(F('x', (x + 1, 1/x))) == 'x0'
    _x = Symbol('x', real=True)
    assert F(('x', _x)) == _x
    assert F((x, _x)) == _x
    assert F('x', real=True).is_real
    y = Symbol('y')
    assert F(('x', y), real=True).is_real
    r = Symbol('x', real=True)
    assert F(('x', r)).is_real
    assert F(('x', r), real=False).is_real
    assert F('x1', Symbol('x1'),
        compare=lambda i: str(i).rstrip('1')).name == 'x0'
    assert F('x1', Symbol('x1'),
        modify=lambda i: i + '_').name == 'x1_'
    assert _symbol(x, _x) == x

