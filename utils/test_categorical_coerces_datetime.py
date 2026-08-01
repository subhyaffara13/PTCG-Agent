
def test_categorical_coerces_datetime(all_parsers):
    parser = all_parsers
    dti = pd.DatetimeIndex(["2017-01-01", "2018-01-01", "2019-01-01"], freq=None)
    dtype = {"b": CategoricalDtype(dti)}

    data = "b\n2017-01-01\n2018-01-01\n2019-01-01"
    expected = DataFrame({"b": Categorical(dtype["b"].categories)})

    result = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(result, expected)

