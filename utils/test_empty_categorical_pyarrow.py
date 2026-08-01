
def test_empty_categorical_pyarrow():
    # https://github.com/pandas-dev/pandas/issues/53077
    pa = pytest.importorskip("pyarrow", "11.0.0")

    arr = [None]
    table = pa.table({"arr": pa.array(arr, "float64").dictionary_encode()})
    exchange_df = table.__dataframe__()
    with tm.assert_produces_warning(match="Interchange"):
        result = pd.api.interchange.from_dataframe(exchange_df)
    expected = pd.DataFrame({"arr": pd.Categorical([np.nan])})
    tm.assert_frame_equal(result, expected)

