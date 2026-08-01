
def test_transform():
    # Also test that 3-way unification is done correctly
    assert Poly(x**2 - 2*x + 1, x).transform(Poly(x + 1), Poly(x - 1)) == \
        Poly(4, x) == \
        cancel((x - 1)**2*(x**2 - 2*x + 1).subs(x, (x + 1)/(x - 1)))

    assert Poly(x**2 - x/2 + 1, x).transform(Poly(x + 1), Poly(x - 1)) == \
        Poly(3*x**2/2 + Rational(5, 2), x) == \
        cancel((x - 1)**2*(x**2 - x/2 + 1).subs(x, (x + 1)/(x - 1)))

    assert Poly(x**2 - 2*x + 1, x).transform(Poly(x + S.Half), Poly(x - 1)) == \
        Poly(Rational(9, 4), x) == \
        cancel((x - 1)**2*(x**2 - 2*x + 1).subs(x, (x + S.Half)/(x - 1)))

    assert Poly(x**2 - 2*x + 1, x).transform(Poly(x + 1), Poly(x - S.Half)) == \
        Poly(Rational(9, 4), x) == \
        cancel((x - S.Half)**2*(x**2 - 2*x + 1).subs(x, (x + 1)/(x - S.Half)))

    # Unify ZZ, QQ, and RR
    assert Poly(x**2 - 2*x + 1, x).transform(Poly(x + 1.0), Poly(x - S.Half)) == \
        Poly(Rational(9, 4), x, domain='RR') == \
        cancel((x - S.Half)**2*(x**2 - 2*x + 1).subs(x, (x + 1.0)/(x - S.Half)))

    raises(ValueError, lambda: Poly(x*y).transform(Poly(x + 1), Poly(x - 1)))
    raises(ValueError, lambda: Poly(x).transform(Poly(y + 1), Poly(x - 1)))
    raises(ValueError, lambda: Poly(x).transform(Poly(x + 1), Poly(y - 1)))
    raises(ValueError, lambda: Poly(x).transform(Poly(x*y + 1), Poly(x - 1)))
    raises(ValueError, lambda: Poly(x).transform(Poly(x + 1), Poly(x*y - 1)))


def test_transform():
    a = Integral(x**2 + 1, (x, -1, 2))
    fx = x
    fy = 3*y + 1
    assert a.doit() == a.transform(fx, fy).doit()
    assert a.transform(fx, fy).transform(fy, fx) == a
    fx = 3*x + 1
    fy = y
    assert a.transform(fx, fy).transform(fy, fx) == a
    a = Integral(sin(1/x), (x, 0, 1))
    assert a.transform(x, 1/y) == Integral(sin(y)/y**2, (y, 1, oo))
    assert a.transform(x, 1/y).transform(y, 1/x) == a
    a = Integral(exp(-x**2), (x, -oo, oo))
    assert a.transform(x, 2*y) == Integral(2*exp(-4*y**2), (y, -oo, oo))
    # < 3 arg limit handled properly
    assert Integral(x, x).transform(x, a*y).doit() == \
        Integral(y*a**2, y).doit()
    _3 = S(3)
    assert Integral(x, (x, 0, -_3)).transform(x, 1/y).doit() == \
        Integral(-1/x**3, (x, -oo, -1/_3)).doit()
    assert Integral(x, (x, 0, _3)).transform(x, 1/y) == \
        Integral(y**(-3), (y, 1/_3, oo))
    # issue 8400
    i = Integral(x + y, (x, 1, 2), (y, 1, 2))
    assert i.transform(x, (x + 2*y, x)).doit() == \
        i.transform(x, (x + 2*z, x)).doit() == 3

    i = Integral(x, (x, a, b))
    assert i.transform(x, 2*s) == Integral(4*s, (s, a/2, b/2))
    raises(ValueError, lambda: i.transform(x, 1))
    raises(ValueError, lambda: i.transform(x, s*t))
    raises(ValueError, lambda: i.transform(x, -s))
    raises(ValueError, lambda: i.transform(x, (s, t)))
    raises(ValueError, lambda: i.transform(2*x, 2*s))

    i = Integral(x**2, (x, 1, 2))
    raises(ValueError, lambda: i.transform(x**2, s))

    am = Symbol('a', negative=True)
    bp = Symbol('b', positive=True)
    i = Integral(x, (x, bp, am))
    i.transform(x, 2*s)
    assert i.transform(x, 2*s) == Integral(-4*s, (s, am/2, bp/2))

    i = Integral(x, (x, a))
    assert i.transform(x, 2*s) == Integral(4*s, (s, a/2))


def test_transform():
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    c = Curve((x, x**2), (x, 0, 1))
    cout = Curve((2*x - 4, 3*x**2 - 10), (x, 0, 1))
    pts = [Point(0, 0), Point(S.Half, Rational(1, 4)), Point(1, 1)]
    pts_out = [Point(-4, -10), Point(-3, Rational(-37, 4)), Point(-2, -7)]

    assert c.scale(2, 3, (4, 5)) == cout
    assert [c.subs(x, xi/2) for xi in Tuple(0, 1, 2)] == pts
    assert [cout.subs(x, xi/2) for xi in Tuple(0, 1, 2)] == pts_out
    assert Curve((x + y, 3*x), (x, 0, 1)).subs(y, S.Half) == \
        Curve((x + S.Half, 3*x), (x, 0, 1))
    assert Curve((x, 3*x), (x, 0, 1)).translate(4, 5) == \
        Curve((x + 4, 3*x + 5), (x, 0, 1))


def test_transform():
    c = Circle((1, 1), 2)
    assert c.scale(-1) == Circle((-1, 1), 2)
    assert c.scale(y=-1) == Circle((1, -1), 2)
    assert c.scale(2) == Ellipse((2, 1), 4, 2)

    assert Ellipse((0, 0), 2, 3).scale(2, 3, (4, 5)) == \
        Ellipse(Point(-4, -10), 4, 9)
    assert Circle((0, 0), 2).scale(2, 3, (4, 5)) == \
        Ellipse(Point(-4, -10), 4, 6)
    assert Ellipse((0, 0), 2, 3).scale(3, 3, (4, 5)) == \
        Ellipse(Point(-8, -10), 6, 9)
    assert Circle((0, 0), 2).scale(3, 3, (4, 5)) == \
        Circle(Point(-8, -10), 6)
    assert Circle(Point(-8, -10), 6).scale(Rational(1, 3), Rational(1, 3), (4, 5)) == \
        Circle((0, 0), 2)
    assert Circle((0, 0), 2).translate(4, 5) == \
        Circle((4, 5), 2)
    assert Circle((0, 0), 2).scale(3, 3) == \
        Circle((0, 0), 6)


def test_transform():
    assert scale(1, 2, (3, 4)).tolist() == \
        [[1, 0, 0], [0, 2, 0], [0, -4, 1]]


def test_transform():
    p = Point(1, 1)
    assert p.transform(rotate(pi/2)) == Point(-1, 1)
    assert p.transform(scale(3, 2)) == Point(3, 2)
    assert p.transform(translate(1, 2)) == Point(2, 3)
    assert Point(1, 1).scale(2, 3, (4, 5)) == \
        Point(-2, -7)
    assert Point(1, 1).translate(4, 5) == \
        Point(5, 6)


def test_transform():
    pts = [Point(0, 0), Point(S.Half, Rational(1, 4)), Point(1, 1)]
    pts_out = [Point(-4, -10), Point(-3, Rational(-37, 4)), Point(-2, -7)]
    assert Triangle(*pts).scale(2, 3, (4, 5)) == Triangle(*pts_out)
    assert RegularPolygon((0, 0), 1, 4).scale(2, 3, (4, 5)) == \
        Polygon(Point(-2, -10), Point(-4, -7), Point(-6, -10), Point(-4, -13))
    # Checks for symmetric scaling
    assert RegularPolygon((0, 0), 1, 4).scale(2, 2) == \
        RegularPolygon(Point2D(0, 0), 2, 4, 0)


def test_transform(string_series, by_row):
    # transforming functions

    with np.errstate(all="ignore"):
        f_sqrt = np.sqrt(string_series)
        f_abs = np.abs(string_series)

        # ufunc
        result = string_series.apply(np.sqrt, by_row=by_row)
        expected = f_sqrt.copy()
        tm.assert_series_equal(result, expected)

        # list-like
        result = string_series.apply([np.sqrt], by_row=by_row)
        expected = f_sqrt.to_frame().copy()
        expected.columns = ["sqrt"]
        tm.assert_frame_equal(result, expected)

        result = string_series.apply(["sqrt"], by_row=by_row)
        tm.assert_frame_equal(result, expected)

        # multiple items in list
        # these are in the order as if we are applying both functions per
        # series and then concatting
        expected = concat([f_sqrt, f_abs], axis=1)
        expected.columns = ["sqrt", "absolute"]
        result = string_series.apply([np.sqrt, np.abs], by_row=by_row)
        tm.assert_frame_equal(result, expected)

        # dict, provide renaming
        expected = concat([f_sqrt, f_abs], axis=1)
        expected.columns = ["foo", "bar"]
        expected = expected.unstack().rename("series")

        result = string_series.apply({"foo": np.sqrt, "bar": np.abs}, by_row=by_row)
        tm.assert_series_equal(result.reindex_like(expected), expected)


def test_transform():
    data = Series(np.arange(9) // 3, index=np.arange(9))

    index = np.arange(9)
    np.random.default_rng(2).shuffle(index)
    data = data.reindex(index)

    grouped = data.groupby(lambda x: x // 3)

    transformed = grouped.transform(lambda x: x * x.sum())
    assert transformed[7] == 12

    # GH 8046
    # make sure that we preserve the input order

    df = DataFrame(
        np.arange(6, dtype="int64").reshape(3, 2), columns=["a", "b"], index=[0, 2, 1]
    )
    key = [0, 0, 1]
    expected = (
        df.sort_index()
        .groupby(key)
        .transform(lambda x: x - x.mean())
        .groupby(key)
        .mean()
    )
    result = df.groupby(key).transform(lambda x: x - x.mean()).groupby(key).mean()
    tm.assert_frame_equal(result, expected)

    def demean(arr):
        return arr - arr.mean(axis=0)

    people = DataFrame(
        np.random.default_rng(2).standard_normal((5, 5)),
        columns=["a", "b", "c", "d", "e"],
        index=["Joe", "Steve", "Wes", "Jim", "Travis"],
    )
    key = ["one", "two", "one", "two", "one"]
    result = people.groupby(key).transform(demean).groupby(key).mean()
    expected = people.groupby(key, group_keys=False).apply(demean).groupby(key).mean()
    tm.assert_frame_equal(result, expected)

    # GH 8430
    df = DataFrame(
        np.random.default_rng(2).standard_normal((50, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=50, freq="B"),
    )
    g = df.groupby(pd.Grouper(freq="ME"))
    g.transform(lambda x: x - 1)

    # GH 9700
    df = DataFrame({"a": range(5, 10), "b": range(5)})
    result = df.groupby("a").transform(max)
    expected = DataFrame({"b": range(5)})
    tm.assert_frame_equal(result, expected)


def test_transform(testcase: DataDrivenTestCase) -> None:
    """Perform an identity transform test case."""

    try:
        src = "\n".join(testcase.input)
        options = parse_options(src, testcase, 1)
        options.use_builtins_fixtures = True
        options.semantic_analysis_only = True
        options.show_traceback = True
        options.reveal_verbose_types = True
        result = build.build(
            sources=[BuildSource("main", None, src)], options=options, alt_lib_path=test_temp_dir
        )
        a = result.errors
        if a:
            raise CompileError(a)
        # Include string representations of the source files in the actual
        # output.
        for module in sorted(result.files.keys()):
            if module in testcase.test_modules:
                t = TypeAssertTransformVisitor()
                t.test_only = True
                file = t.mypyfile(result.files[module])
                a += file.str_with_options(options).split("\n")
    except CompileError as e:
        a = e.messages
    if testcase.normalize_output:
        a = normalize_error_messages(a)
    assert_string_arrays_equal(
        testcase.output,
        a,
        f"Invalid semantic analyzer output ({testcase.file}, line {testcase.line})",
    )


def test_transform():
    obj = TransformBlob()
    pf = pickle.dumps(obj)
    del obj

    obj = pickle.loads(pf)
    # Check parent -> child links of TransformWrapper.
    assert obj.wrapper._child == obj.composite
    # Check child -> parent links of TransformWrapper.
    assert [v() for v in obj.wrapper._parents.values()] == [obj.composite2]
    # Check input and output dimensions are set as expected.
    assert obj.wrapper.input_dims == obj.composite.input_dims
    assert obj.wrapper.output_dims == obj.composite.output_dims

