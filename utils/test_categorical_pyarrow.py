
def test_categorical_pyarrow():
    # GH 49889
    pa = pytest.importorskip("pyarrow", "11.0.0")

    arr = ["Mon", "Tue", "Mon", "Wed", "Mon", "Thu", "Fri", "Sat", "Sun"]
    table = pa.table({"weekday": pa.array(arr).dictionary_encode()})
    exchange_df = table.__dataframe__()
    with tm.assert_produces_warning(match="Interchange"):
        result = from_dataframe(exchange_df)
    weekday = pd.Categorical(
        arr, categories=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    )
    expected = pd.DataFrame({"weekday": weekday})
    tm.assert_frame_equal(result, expected)

