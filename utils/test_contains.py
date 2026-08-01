
def test_contains():
    assert 6 in ConditionSet(x, x > 5, Interval(1, 7))
    assert (8 in ConditionSet(x, y > 5, Interval(1, 7))) is False
    # `in` should give True or False; in this case there is not
    # enough information for that result
    raises(TypeError,
        lambda: 6 in ConditionSet(x, y > 5, Interval(1, 7)))
    # here, there is enough information but the comparison is
    # not defined
    raises(TypeError, lambda: 0 in ConditionSet(x, 1/x >= 0, S.Reals))
    assert ConditionSet(x, y > 5, Interval(1, 7)
        ).contains(6) == (y > 5)
    assert ConditionSet(x, y > 5, Interval(1, 7)
        ).contains(8) is S.false
    assert ConditionSet(x, y > 5, Interval(1, 7)
        ).contains(w) == And(Contains(w, Interval(1, 7)), y > 5)
    # This returns an unevaluated Contains object
    # because 1/0 should not be defined for 1 and 0 in the context of
    # reals.
    assert ConditionSet(x, 1/x >= 0, S.Reals).contains(0) == \
        Contains(0, ConditionSet(x, 1/x >= 0, S.Reals), evaluate=False)
    c = ConditionSet((x, y), x + y > 1, S.Integers**2)
    assert not c.contains(1)
    assert c.contains((2, 1))
    assert not c.contains((0, 1))
    c = ConditionSet((w, (x, y)), w + x + y > 1, S.Integers*S.Integers**2)
    assert not c.contains(1)
    assert not c.contains((1, 2))
    assert not c.contains(((1, 2), 3))
    assert not c.contains(((1, 2), (3, 4)))
    assert c.contains((1, (3, 4)))


def test_contains():
    assert Interval(0, 2).contains(1) is S.true
    assert Interval(0, 2).contains(3) is S.false
    assert Interval(0, 2, True, False).contains(0) is S.false
    assert Interval(0, 2, True, False).contains(2) is S.true
    assert Interval(0, 2, False, True).contains(0) is S.true
    assert Interval(0, 2, False, True).contains(2) is S.false
    assert Interval(0, 2, True, True).contains(0) is S.false
    assert Interval(0, 2, True, True).contains(2) is S.false

    assert (Interval(0, 2) in Interval(0, 2)) is False

    assert FiniteSet(1, 2, 3).contains(2) is S.true
    assert FiniteSet(1, 2, Symbol('x')).contains(Symbol('x')) is S.true

    assert FiniteSet(y)._contains(x) == Eq(y, x, evaluate=False)
    raises(TypeError, lambda: x in FiniteSet(y))
    assert FiniteSet({x, y})._contains({x}) == Eq({x, y}, {x}, evaluate=False)
    assert FiniteSet({x, y}).subs(y, x)._contains({x}) is S.true
    assert FiniteSet({x, y}).subs(y, x+1)._contains({x}) is S.false

    # issue 8197
    from sympy.abc import a, b
    assert FiniteSet(b).contains(-a) == Eq(b, -a)
    assert FiniteSet(b).contains(a) == Eq(b, a)
    assert FiniteSet(a).contains(1) == Eq(a, 1)
    raises(TypeError, lambda: 1 in FiniteSet(a))

    # issue 8209
    rad1 = Pow(Pow(2, Rational(1, 3)) - 1, Rational(1, 3))
    rad2 = Pow(Rational(1, 9), Rational(1, 3)) - Pow(Rational(2, 9), Rational(1, 3)) + Pow(Rational(4, 9), Rational(1, 3))
    s1 = FiniteSet(rad1)
    s2 = FiniteSet(rad2)
    assert s1 - s2 == S.EmptySet

    items = [1, 2, S.Infinity, S('ham'), -1.1]
    fset = FiniteSet(*items)
    assert all(item in fset for item in items)
    assert all(fset.contains(item) is S.true for item in items)

    assert Union(Interval(0, 1), Interval(2, 5)).contains(3) is S.true
    assert Union(Interval(0, 1), Interval(2, 5)).contains(6) is S.false
    assert Union(Interval(0, 1), FiniteSet(2, 5)).contains(3) is S.false

    assert S.EmptySet.contains(1) is S.false
    assert FiniteSet(rootof(x**3 + x - 1, 0)).contains(S.Infinity) is S.false

    assert rootof(x**5 + x**3 + 1, 0) in S.Reals
    assert not rootof(x**5 + x**3 + 1, 1) in S.Reals

    # non-bool results
    assert Union(Interval(1, 2), Interval(3, 4)).contains(x) == \
        Or(And(S.One <= x, x <= 2), And(S(3) <= x, x <= 4))
    assert Intersection(Interval(1, x), Interval(2, 3)).contains(y) == \
        And(y <= 3, y <= x, S.One <= y, S(2) <= y)

    assert (S.Complexes).contains(S.ComplexInfinity) == S.false


def test_contains():
    assert Order(1, x) not in Order(1)
    assert Order(1) in Order(1, x)
    raises(TypeError, lambda: Order(x*y**2) in Order(x**2*y))


def test_contains():
    p1 = Point(0, 0)

    r = Ray(p1, Point(4, 4))
    r1 = Ray3D(p1, Point3D(0, 0, -1))
    r2 = Ray3D(p1, Point3D(0, 1, 0))
    r3 = Ray3D(p1, Point3D(0, 0, 1))

    l = Line(Point(0, 1), Point(3, 4))
    # Segment contains
    assert Point(0, (a + b) / 2) in Segment((0, a), (0, b))
    assert Point((a + b) / 2, 0) in Segment((a, 0), (b, 0))
    assert Point3D(0, 1, 0) in Segment3D((0, 1, 0), (0, 1, 0))
    assert Point3D(1, 0, 0) in Segment3D((1, 0, 0), (1, 0, 0))
    assert Segment3D(Point3D(0, 0, 0), Point3D(1, 0, 0)).contains([]) is True
    assert Segment3D(Point3D(0, 0, 0), Point3D(1, 0, 0)).contains(
        Segment3D(Point3D(2, 2, 2), Point3D(3, 2, 2))) is False
    # Line contains
    assert l.contains(Point(0, 1)) is True
    assert l.contains((0, 1)) is True
    assert l.contains((0, 0)) is False
    # Ray contains
    assert r.contains(p1) is True
    assert r.contains((1, 1)) is True
    assert r.contains((1, 3)) is False
    assert r.contains(Segment((1, 1), (2, 2))) is True
    assert r.contains(Segment((1, 2), (2, 5))) is False
    assert r.contains(Ray((2, 2), (3, 3))) is True
    assert r.contains(Ray((2, 2), (3, 5))) is False
    assert r1.contains(Segment3D(p1, Point3D(0, 0, -10))) is True
    assert r1.contains(Segment3D(Point3D(1, 1, 1), Point3D(2, 2, 2))) is False
    assert r2.contains(Point3D(0, 0, 0)) is True
    assert r3.contains(Point3D(0, 0, 0)) is True
    assert Ray3D(Point3D(1, 1, 1), Point3D(1, 0, 0)).contains([]) is False
    assert Line3D((0, 0, 0), (x, y, z)).contains((2 * x, 2 * y, 2 * z))
    with warns(UserWarning, test_stacklevel=False):
        assert Line3D(p1, Point3D(0, 1, 0)).contains(Point(1.0, 1.0)) is False

    with warns(UserWarning, test_stacklevel=False):
        assert r3.contains(Point(1.0, 1.0)) is False


def test_contains(n):
    elements = get_elements(n)
    dis = DisjointSet(elements)
    for x in elements:
        assert x in dis

    assert "dummy" not in dis


def test_contains():
    # Python 3.14 changes the message from "is not iterable" to
    # "is not a container or iterable"
    with pytest.raises(
        TypeError, match="argument of type 'Expression' is not .*iterable"
    ):
        1 in pd.col("a")


def test_contains(any_string_dtype):
    values = np.array(
        ["foo", np.nan, "fooommm__foo", "mmm_", "foommm[_]+bar"], dtype=np.object_
    )
    values = Series(values, dtype=any_string_dtype)
    pat = "mmm[_]+"

    result = values.str.contains(pat)
    if any_string_dtype == "str":
        # NaN propagates as False
        expected = Series([False, False, True, True, False], dtype=bool)
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        expected = Series(
            np.array([False, np.nan, True, True, False], dtype=np.object_),
            dtype=expected_dtype,
        )

    tm.assert_series_equal(result, expected)

    result = values.str.contains(pat, regex=False)
    if any_string_dtype == "str":
        expected = Series([False, False, False, False, True], dtype=bool)
    else:
        expected = Series(
            np.array([False, np.nan, False, False, True], dtype=np.object_),
            dtype=expected_dtype,
        )
    tm.assert_series_equal(result, expected)

    values = Series(
        np.array(["foo", "xyz", "fooommm__foo", "mmm_"], dtype=object),
        dtype=any_string_dtype,
    )
    result = values.str.contains(pat)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series(np.array([False, False, True, True]), dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # case insensitive using regex
    values = Series(
        np.array(["Foo", "xYz", "fOOomMm__fOo", "MMM_"], dtype=object),
        dtype=any_string_dtype,
    )

    result = values.str.contains("FOO|mmm", case=False)
    expected = Series(np.array([True, False, True, True]), dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # case insensitive without regex
    result = values.str.contains("foo", regex=False, case=False)
    expected = Series(np.array([True, False, True, False]), dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    # unicode
    values = Series(
        np.array(["foo", np.nan, "fooommm__foo", "mmm_"], dtype=np.object_),
        dtype=any_string_dtype,
    )
    pat = "mmm[_]+"

    result = values.str.contains(pat)
    if any_string_dtype == "str":
        expected = Series([False, False, True, True], dtype=bool)
    else:
        expected_dtype = (
            "object" if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
        )
        expected = Series(
            np.array([False, np.nan, True, True], dtype=np.object_),
            dtype=expected_dtype,
        )
    tm.assert_series_equal(result, expected)

    result = values.str.contains(pat, na=False)
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )
    expected = Series(np.array([False, False, True, True]), dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    values = Series(
        np.array(["foo", "xyz", "fooommm__foo", "mmm_"], dtype=np.object_),
        dtype=any_string_dtype,
    )
    result = values.str.contains(pat)
    expected = Series(np.array([False, False, True, True]), dtype=expected_dtype)
    tm.assert_series_equal(result, expected)


def test_contains(temp_hdfstore):
    store = temp_hdfstore
    store["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    store["b"] = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    store["foo/bar"] = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    assert "a" in store
    assert "b" in store
    assert "c" not in store
    assert "foo/bar" in store
    assert "/foo/bar" in store
    assert "/foo/b" not in store
    assert "bar" not in store

    # gh-2694: tables.NaturalNameWarning
    with tm.assert_produces_warning(tables.NaturalNameWarning, check_stacklevel=False):
        store["node())"] = DataFrame(
            1.1 * np.arange(120).reshape((30, 4)),
            columns=Index(list("ABCD"), dtype=object),
            index=Index([f"i-{i}" for i in range(30)], dtype=object),
        )
    assert "node())" in store


def test_contains():
    fig = plt.figure(figsize=(8, 6))
    ax = plt.axes()

    mevent = MouseEvent('button_press_event', fig.canvas, 0.5, 0.5, 1, None)

    xs = np.linspace(0.25, 0.75, 30)
    ys = np.linspace(0.25, 0.75, 30)
    xs, ys = np.meshgrid(xs, ys)

    txt = plt.text(
        0.5, 0.4, 'hello world', ha='center', fontsize=30, rotation=30)
    # uncomment to draw the text's bounding box
    # txt.set_bbox(dict(edgecolor='black', facecolor='none'))

    # draw the text. This is important, as the contains method can only work
    # when a renderer exists.
    fig.canvas.draw()

    for x, y in zip(xs.flat, ys.flat):
        mevent.x, mevent.y = plt.gca().transAxes.transform([x, y])
        contains, _ = txt.contains(mevent)
        color = 'yellow' if contains else 'red'

        # capture the viewLim, plot a point, and reset the viewLim
        vl = ax.viewLim.frozen()
        ax.plot(x, y, 'o', color=color)
        ax.viewLim.set(vl)

