
def test_basic_string(using_infer_string):
    # GH 8623
    x = DataFrame(
        [[1, "John P. Doe"], [2, "Jane Dove"], [1, "John P. Doe"]],
        columns=["person_id", "person_name"],
    )
    x["person_name"] = Categorical(x.person_name)

    g = x.groupby(["person_id"], observed=False)
    result = g.transform(lambda x: x)
    tm.assert_frame_equal(result, x[["person_name"]])

    result = x.drop_duplicates("person_name")
    expected = x.iloc[[0, 1]]
    tm.assert_frame_equal(result, expected)

    def f(x):
        return x.drop_duplicates("person_name").iloc[0]

    result = g.apply(f)
    expected = x[["person_name"]].iloc[[0, 1]]
    expected.index = Index([1, 2], name="person_id")
    dtype = "str" if using_infer_string else object
    expected["person_name"] = expected["person_name"].astype(dtype)
    tm.assert_frame_equal(result, expected)


def test_basic_string(styler):
    result = styler.to_string()
    expected = dedent(
        """\
     A B C
    0 0 -0.61 ab
    1 1 -1.22 cd
    """
    )
    assert result == expected


def test_basic_string():
    """
    Test basic string conversion
    """
    mp.dps = 15
    assert mpf('3') == mpf('3.0') == mpf('0003.') == mpf('0.03e2') == mpf(3.0)
    assert mpf('30') == mpf('30.0') == mpf('00030.') == mpf(30.0)
    for i in range(10):
        for j in range(10):
            assert mpf('%ie%i' % (i,j)) == i * 10**j
    assert str(mpf('25000.0')) == '25000.0'
    assert str(mpf('2500.0')) == '2500.0'
    assert str(mpf('250.0')) == '250.0'
    assert str(mpf('25.0')) == '25.0'
    assert str(mpf('2.5')) == '2.5'
    assert str(mpf('0.25')) == '0.25'
    assert str(mpf('0.025')) == '0.025'
    assert str(mpf('0.0025')) == '0.0025'
    assert str(mpf('0.00025')) == '0.00025'
    assert str(mpf('0.000025')) == '2.5e-5'
    assert str(mpf(0)) == '0.0'
    assert str(mpf('2.5e1000000000000000000000')) == '2.5e+1000000000000000000000'
    assert str(mpf('2.6e-1000000000000000000000')) == '2.6e-1000000000000000000000'
    assert str(mpf(1.23402834e-15)) == '1.23402834e-15'
    assert str(mpf(-1.23402834e-15)) == '-1.23402834e-15'
    assert str(mpf(-1.2344e-15)) == '-1.2344e-15'
    assert repr(mpf(-1.2344e-15)) == "mpf('-1.2343999999999999e-15')"
    assert str(mpf("2163048125L")) == '2163048125.0'
    assert str(mpf("-2163048125l")) == '-2163048125.0'
    assert str(mpf("-2163048125L/1088391168")) == '-1.98738118113799'
    assert str(mpf("2163048125/1088391168l")) == '1.98738118113799'

