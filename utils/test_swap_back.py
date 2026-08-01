
def test_swap_back():
    f, g = map(Function, 'fg')
    fx, gx = f(x), g(x)
    assert solve([fx + y - 2, fx - gx - 5], fx, y, gx) == \
        {fx: gx + 5, y: -gx - 3}
    assert solve(fx + gx*x - 2, [fx, gx], dict=True) == [{fx: 2, gx: 0}]
    assert solve(fx + gx**2*x - y, [fx, gx], dict=True) == [{fx: y, gx: 0}]
    assert solve([f(1) - 2, x + 2], dict=True) == [{x: -2, f(1): 2}]

