
def test_preserve_dtypes(op, using_python_scalars):
    df = pd.DataFrame(
        {
            "A": ["a", "b", "b"],
            "B": [1, None, 3],
            "C": pd.array([0.1, None, 3.0], dtype="Float64"),
        }
    )

    # op
    result = getattr(df.C, op)()
    if using_python_scalars:
        assert type(result) == float
    else:
        assert isinstance(result, np.float64)

    # groupby
    result = getattr(df.groupby("A"), op)()

    expected = pd.DataFrame(
        {"B": np.array([1.0, 3.0]), "C": pd.array([0.1, 3], dtype="Float64")},
        index=pd.Index(["a", "b"], name="A"),
    )
    tm.assert_frame_equal(result, expected)


def test_preserve_dtypes(op, using_python_scalars):
    # for ops that enable (mean would actually work here
    # but generally it is a float return value)
    df = pd.DataFrame(
        {
            "A": ["a", "b", "b"],
            "B": [1, None, 3],
            "C": pd.array([1, None, 3], dtype="Int64"),
        }
    )

    # op
    result = getattr(df.C, op)()
    if op in {"sum", "prod", "min", "max"} and not using_python_scalars:
        assert isinstance(result, np.int64)
    else:
        assert isinstance(result, int)

    # groupby
    result = getattr(df.groupby("A"), op)()

    expected = pd.DataFrame(
        {"B": np.array([1.0, 3.0]), "C": pd.array([1, 3], dtype="Int64")},
        index=pd.Index(["a", "b"], name="A"),
    )
    tm.assert_frame_equal(result, expected)

