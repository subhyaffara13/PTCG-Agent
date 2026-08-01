
def test_boolean(value: t.Any) -> bool:
    """Return true if the object is a boolean value.

    .. versionadded:: 2.11
    """
    return value is True or value is False


def test_boolean():
    assert julia_code(x & y) == "x && y"
    assert julia_code(x | y) == "x || y"
    assert julia_code(~x) == "!x"
    assert julia_code(x & y & z) == "x && y && z"
    assert julia_code(x | y | z) == "x || y || z"
    assert julia_code((x & y) | z) == "z || x && y"
    assert julia_code((x | y) & z) == "z && (x || y)"


def test_boolean():
    assert maple_code(x & y) == "x and y"
    assert maple_code(x | y) == "x or y"
    assert maple_code(~x) == "not x"
    assert maple_code(x & y & z) == "x and y and z"
    assert maple_code(x | y | z) == "x or y or z"
    assert maple_code((x & y) | z) == "z or x and y"
    assert maple_code((x | y) & z) == "z and (x or y)"


def test_boolean():
    assert mcode(x & y) == "x & y"
    assert mcode(x | y) == "x | y"
    assert mcode(~x) == "~x"
    assert mcode(x & y & z) == "x & y & z"
    assert mcode(x | y | z) == "x | y | z"
    assert mcode((x & y) | z) == "z | x & y"
    assert mcode((x | y) & z) == "z & (x | y)"


def test_boolean():
    assert rust_code(True) == "true"
    assert rust_code(S.true) == "true"
    assert rust_code(False) == "false"
    assert rust_code(S.false) == "false"
    assert rust_code(k & m) == "k && m"
    assert rust_code(k | m) == "k || m"
    assert rust_code(~k) == "!k"
    assert rust_code(k & m & n) == "k && m && n"
    assert rust_code(k | m | n) == "k || m || n"
    assert rust_code((k & m) | n) == "n || k && m"
    assert rust_code((k | m) & n) == "n && (k || m)"


def test_boolean():
    with _check_warns([]) as w:
        assert smtlib_code(x & y, log_warn=w) == '(declare-const x Bool)\n' \
                                                 '(declare-const y Bool)\n' \
                                                 '(assert (and x y))'
        assert smtlib_code(x | y, log_warn=w) == '(declare-const x Bool)\n' \
                                                 '(declare-const y Bool)\n' \
                                                 '(assert (or x y))'
        assert smtlib_code(~x, log_warn=w) == '(declare-const x Bool)\n' \
                                              '(assert (not x))'
        assert smtlib_code(x & y & z, log_warn=w) == '(declare-const x Bool)\n' \
                                                     '(declare-const y Bool)\n' \
                                                     '(declare-const z Bool)\n' \
                                                     '(assert (and x y z))'

    with _check_warns([_W.DEFAULTING_TO_FLOAT]) as w:
        assert smtlib_code((x & ~y) | (z > 3), log_warn=w) == '(declare-const x Bool)\n' \
                                                              '(declare-const y Bool)\n' \
                                                              '(declare-const z Real)\n' \
                                                              '(assert (or (> z 3) (and x (not y))))'

    f = Function('f')
    g = Function('g')
    h = Function('h')
    with _check_warns([_W.DEFAULTING_TO_FLOAT]) as w:
        assert smtlib_code(
            [Gt(f(x), y),
             Lt(y, g(z))],
            symbol_table={
                f: Callable[[bool], int], g: Callable[[bool], int],
            }, log_warn=w
        ) == '(declare-const x Bool)\n' \
             '(declare-const y Real)\n' \
             '(declare-const z Bool)\n' \
             '(declare-fun f (Bool) Int)\n' \
             '(declare-fun g (Bool) Int)\n' \
             '(assert (> (f x) y))\n' \
             '(assert (< y (g z)))'

    with _check_warns([]) as w:
        assert smtlib_code(
            [Eq(f(x), y),
             Lt(y, g(z))],
            symbol_table={
                f: Callable[[bool], int], g: Callable[[bool], int],
            }, log_warn=w
        ) == '(declare-const x Bool)\n' \
             '(declare-const y Int)\n' \
             '(declare-const z Bool)\n' \
             '(declare-fun f (Bool) Int)\n' \
             '(declare-fun g (Bool) Int)\n' \
             '(assert (= (f x) y))\n' \
             '(assert (< y (g z)))'

    with _check_warns([]) as w:
        assert smtlib_code(
            [Eq(f(x), y),
             Eq(g(f(x)), z),
             Eq(h(g(f(x))), x)],
            symbol_table={
                f: Callable[[float], int],
                g: Callable[[int], bool],
                h: Callable[[bool], float]
            },
            log_warn=w
        ) == '(declare-const x Real)\n' \
             '(declare-const y Int)\n' \
             '(declare-const z Bool)\n' \
             '(declare-fun f (Real) Int)\n' \
             '(declare-fun g (Int) Bool)\n' \
             '(declare-fun h (Bool) Real)\n' \
             '(assert (= (f x) y))\n' \
             '(assert (= (g (f x)) z))\n' \
             '(assert (= (h (g (f x))) x))'


def test_boolean():
    # There can be 9*9 test cases in full mapping of the cartesian product.
    # But we only consider 3*3 cases for simplicity.
    s = [
        intervalMembership(False, False),
        intervalMembership(None, None),
        intervalMembership(True, True)
    ]

    # Reduced tests for 'And'
    a1 = [
        intervalMembership(False, False),
        intervalMembership(False, False),
        intervalMembership(False, False),
        intervalMembership(False, False),
        intervalMembership(None, None),
        intervalMembership(None, None),
        intervalMembership(False, False),
        intervalMembership(None, None),
        intervalMembership(True, True)
    ]
    a1_iter = iter(a1)
    for i in range(len(s)):
        for j in range(len(s)):
            assert s[i] & s[j] == next(a1_iter)

    # Reduced tests for 'Or'
    a1 = [
        intervalMembership(False, False),
        intervalMembership(None, False),
        intervalMembership(True, False),
        intervalMembership(None, False),
        intervalMembership(None, None),
        intervalMembership(True, None),
        intervalMembership(True, False),
        intervalMembership(True, None),
        intervalMembership(True, True)
    ]
    a1_iter = iter(a1)
    for i in range(len(s)):
        for j in range(len(s)):
            assert s[i] | s[j] == next(a1_iter)

    # Reduced tests for 'Xor'
    a1 = [
        intervalMembership(False, False),
        intervalMembership(None, False),
        intervalMembership(True, False),
        intervalMembership(None, False),
        intervalMembership(None, None),
        intervalMembership(None, None),
        intervalMembership(True, False),
        intervalMembership(None, None),
        intervalMembership(False, True)
    ]
    a1_iter = iter(a1)
    for i in range(len(s)):
        for j in range(len(s)):
            assert s[i] ^ s[j] == next(a1_iter)

    # Reduced tests for 'Not'
    a1 = [
        intervalMembership(True, False),
        intervalMembership(None, None),
        intervalMembership(False, True)
    ]
    a1_iter = iter(a1)
    for i in range(len(s)):
        assert ~s[i] == next(a1_iter)

