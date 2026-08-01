
def test_replace():
    assert replace('abc', ('a', 'b')) == 'bbc'
    assert replace('abc', {'a': 'Aa'}) == 'Aabc'
    assert replace('abc', ('a', 'b'), ('c', 'C')) == 'bbC'


def test_replace():
    F, G = symbols('F, G', cls=Function)
    K = OperationsOnlyMatrix(2, 2, lambda i, j: G(i+j))
    M = OperationsOnlyMatrix(2, 2, lambda i, j: F(i+j))
    N = M.replace(F, G)
    assert N == K


def test_replace():
    F, G = symbols('F, G', cls=Function)
    K = Matrix(2, 2, lambda i, j: G(i+j))
    M = Matrix(2, 2, lambda i, j: F(i+j))
    N = M.replace(F, G)
    assert N == K


def test_replace():
    F, G = symbols('F, G', cls=Function)
    K = Matrix(2, 2, lambda i, j: G(i+j))
    M = Matrix(2, 2, lambda i, j: F(i+j))
    N = M.replace(F, G)
    assert N == K


def test_replace():
    e = log(sin(x)) + tan(sin(x**2))

    assert e.replace(sin, cos) == log(cos(x)) + tan(cos(x**2))
    assert e.replace(
        sin, lambda a: sin(2*a)) == log(sin(2*x)) + tan(sin(2*x**2))

    a = Wild('a')
    b = Wild('b')

    assert e.replace(sin(a), cos(a)) == log(cos(x)) + tan(cos(x**2))
    assert e.replace(
        sin(a), lambda a: sin(2*a)) == log(sin(2*x)) + tan(sin(2*x**2))
    # test exact
    assert (2*x).replace(a*x + b, b - a, exact=True) == 2*x
    assert (2*x).replace(a*x + b, b - a) == 2*x
    assert (2*x).replace(a*x + b, b - a, exact=False) == 2/x
    assert (2*x).replace(a*x + b, lambda a, b: b - a, exact=True) == 2*x
    assert (2*x).replace(a*x + b, lambda a, b: b - a) == 2*x
    assert (2*x).replace(a*x + b, lambda a, b: b - a, exact=False) == 2/x

    g = 2*sin(x**3)

    assert g.replace(
        lambda expr: expr.is_Number, lambda expr: expr**2) == 4*sin(x**9)

    assert cos(x).replace(cos, sin, map=True) == (sin(x), {cos(x): sin(x)})
    assert sin(x).replace(cos, sin) == sin(x)

    cond, func = lambda x: x.is_Mul, lambda x: 2*x
    assert (x*y).replace(cond, func, map=True) == (2*x*y, {x*y: 2*x*y})
    assert (x*(1 + x*y)).replace(cond, func, map=True) == \
        (2*x*(2*x*y + 1), {x*(2*x*y + 1): 2*x*(2*x*y + 1), x*y: 2*x*y})
    assert (y*sin(x)).replace(sin, lambda expr: sin(expr)/y, map=True) == \
        (sin(x), {sin(x): sin(x)/y})
    # if not simultaneous then y*sin(x) -> y*sin(x)/y = sin(x) -> sin(x)/y
    assert (y*sin(x)).replace(sin, lambda expr: sin(expr)/y,
        simultaneous=False) == sin(x)/y
    assert (x**2 + O(x**3)).replace(Pow, lambda b, e: b**e/e
        ) == x**2/2 + O(x**3)
    assert (x**2 + O(x**3)).replace(Pow, lambda b, e: b**e/e,
        simultaneous=False) == x**2/2 + O(x**3)
    assert (x*(x*y + 3)).replace(lambda x: x.is_Mul, lambda x: 2 + x) == \
        x*(x*y + 5) + 2
    e = (x*y + 1)*(2*x*y + 1) + 1
    assert e.replace(cond, func, map=True) == (
        2*((2*x*y + 1)*(4*x*y + 1)) + 1,
        {2*x*y: 4*x*y, x*y: 2*x*y, (2*x*y + 1)*(4*x*y + 1):
        2*((2*x*y + 1)*(4*x*y + 1))})
    assert x.replace(x, y) == y
    assert (x + 1).replace(1, 2) == x + 2

    # https://groups.google.com/forum/#!topic/sympy/8wCgeC95tz0
    n1, n2, n3 = symbols('n1:4', commutative=False)
    assert (n1*f(n2)).replace(f, lambda x: x) == n1*n2
    assert (n3*f(n2)).replace(f, lambda x: x) == n3*n2

    # issue 16725
    assert S.Zero.replace(Wild('x'), 1) == 1
    # let the user override the default decision of False
    assert S.Zero.replace(Wild('x'), 1, exact=True) == 0


def test_replace(replace_kwargs):
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    df_replaced = df.replace(**replace_kwargs)

    if (df_replaced["b"] == df["b"]).all():
        assert np.shares_memory(get_array(df_replaced, "b"), get_array(df, "b"))
    assert tm.shares_memory(get_array(df_replaced, "c"), get_array(df, "c"))

    # mutating squeezed df triggers a copy-on-write for that column/block
    df_replaced.loc[0, "c"] = -1
    assert not np.shares_memory(get_array(df_replaced, "c"), get_array(df, "c"))

    if "a" in replace_kwargs["to_replace"]:
        arr = get_array(df_replaced, "a")
        df_replaced.loc[0, "a"] = 100
        assert np.shares_memory(get_array(df_replaced, "a"), arr)
    tm.assert_frame_equal(df, df_orig)


def test_replace(any_string_dtype):
    ser = Series(["fooBAD__barBAD", np.nan], dtype=any_string_dtype)

    result = ser.str.replace("BAD[_]*", "", regex=True)
    expected = Series(["foobar", np.nan], dtype=any_string_dtype)
    tm.assert_series_equal(result, expected)

