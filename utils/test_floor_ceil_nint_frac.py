
def test_floor_ceil_nint_frac():
    mp.dps = 15
    for n in range(-10,10):
        assert floor(n) == n
        assert floor(n+0.5) == n
        assert ceil(n) == n
        assert ceil(n+0.5) == n+1
        assert nint(n) == n
        # nint rounds to even
        if n % 2 == 1:
            assert nint(n+0.5) == n+1
        else:
            assert nint(n+0.5) == n
    assert floor(inf) == inf
    assert floor(ninf) == ninf
    assert isnan(floor(nan))
    assert ceil(inf) == inf
    assert ceil(ninf) == ninf
    assert isnan(ceil(nan))
    assert nint(inf) == inf
    assert nint(ninf) == ninf
    assert isnan(nint(nan))
    assert floor(0.1) == 0
    assert floor(0.9) == 0
    assert floor(-0.1) == -1
    assert floor(-0.9) == -1
    assert floor(10000000000.1) == 10000000000
    assert floor(10000000000.9) == 10000000000
    assert floor(-10000000000.1) == -10000000000-1
    assert floor(-10000000000.9) == -10000000000-1
    assert floor(1e-100) == 0
    assert floor(-1e-100) == -1
    assert floor(1e100) == 1e100
    assert floor(-1e100) == -1e100
    assert ceil(0.1) == 1
    assert ceil(0.9) == 1
    assert ceil(-0.1) == 0
    assert ceil(-0.9) == 0
    assert ceil(10000000000.1) == 10000000000+1
    assert ceil(10000000000.9) == 10000000000+1
    assert ceil(-10000000000.1) == -10000000000
    assert ceil(-10000000000.9) == -10000000000
    assert ceil(1e-100) == 1
    assert ceil(-1e-100) == 0
    assert ceil(1e100) == 1e100
    assert ceil(-1e100) == -1e100
    assert nint(0.1) == 0
    assert nint(0.9) == 1
    assert nint(-0.1) == 0
    assert nint(-0.9) == -1
    assert nint(10000000000.1) == 10000000000
    assert nint(10000000000.9) == 10000000000+1
    assert nint(-10000000000.1) == -10000000000
    assert nint(-10000000000.9) == -10000000000-1
    assert nint(1e-100) == 0
    assert nint(-1e-100) == 0
    assert nint(1e100) == 1e100
    assert nint(-1e100) == -1e100
    assert floor(3.2+4.6j) == 3+4j
    assert ceil(3.2+4.6j) == 4+5j
    assert nint(3.2+4.6j) == 3+5j
    for n in range(-10,10):
        assert frac(n) == 0
    assert frac(0.25) == 0.25
    assert frac(1.25) == 0.25
    assert frac(2.25) == 0.25
    assert frac(-0.25) == 0.75
    assert frac(-1.25) == 0.75
    assert frac(-2.25) == 0.75
    assert frac('1e100000000000000') == 0
    u = mpf('1e-100000000000000')
    assert frac(u) == u
    assert frac(-u) == 1  # rounding!
    u = mpf('1e-400')
    assert frac(-u, prec=0) == fsub(1, u, exact=True)
    assert frac(3.25+4.75j) == 0.25+0.75j

