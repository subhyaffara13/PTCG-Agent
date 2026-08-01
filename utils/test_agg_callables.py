
def test_agg_callables():
    # GH 7929
    df = DataFrame({"foo": [1, 2], "bar": [3, 4]}).astype(np.int64)

    class fn_class:
        def __call__(self, x):
            return sum(x)

    equiv_callables = [
        sum,
        np.sum,
        lambda x: sum(x),
        lambda x: x.sum(),
        partial(sum),
        fn_class(),
    ]

    expected = df.groupby("foo").agg("sum")
    for ecall in equiv_callables:
        result = df.groupby("foo").agg(ecall)
        tm.assert_frame_equal(result, expected)

