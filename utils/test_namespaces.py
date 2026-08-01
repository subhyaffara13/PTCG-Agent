
def test_namespaces():
    ns1 = {}
    ns2 = {}

    def foo(x):
        return 1
    foo1 = orig_dispatch(int, namespace=ns1)(foo)

    def foo(x):
        return 2
    foo2 = orig_dispatch(int, namespace=ns2)(foo)

    assert foo1(0) == 1
    assert foo2(0) == 2


def test_namespaces(
    expr: Expression, expected_values: list[object], expected_str: str
) -> None:
    df = pd.DataFrame({"a": [datetime(2020, 1, 1)], "b": ["foo"]})
    result = df.assign(c=expr)
    expected = pd.DataFrame(
        {"a": [datetime(2020, 1, 1)], "b": ["foo"], "c": expected_values}
    )
    tm.assert_frame_equal(result, expected, check_dtype=False)
    assert str(expr) == expected_str

