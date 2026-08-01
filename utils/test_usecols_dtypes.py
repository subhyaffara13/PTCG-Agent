
def test_usecols_dtypes(c_parser_only, using_infer_string):
    parser = c_parser_only
    data = """\
1,2,3
4,5,6
7,8,9
10,11,12"""

    result = parser.read_csv(
        StringIO(data),
        usecols=(0, 1, 2),
        names=("a", "b", "c"),
        header=None,
        converters={"a": str},
        dtype={"b": int, "c": float},
    )
    result2 = parser.read_csv(
        StringIO(data),
        usecols=(0, 2),
        names=("a", "b", "c"),
        header=None,
        converters={"a": str},
        dtype={"b": int, "c": float},
    )

    if using_infer_string:
        assert (result.dtypes == ["string", int, float]).all()
        assert (result2.dtypes == ["string", float]).all()
    else:
        assert (result.dtypes == [object, int, float]).all()
        assert (result2.dtypes == [object, float]).all()

