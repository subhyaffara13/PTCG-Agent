
def test_large_string_pyarrow():
    # GH 52795
    pa = pytest.importorskip("pyarrow", "11.0.0")

    arr = ["Mon", "Tue"]
    table = pa.table({"weekday": pa.array(arr, "large_string")})
    exchange_df = table.__dataframe__()
    with tm.assert_produces_warning(match="Interchange"):
        result = from_dataframe(exchange_df)
    expected = pd.DataFrame({"weekday": ["Mon", "Tue"]})
    tm.assert_frame_equal(result, expected)

    # check round-trip
    # Don't check stacklevel as PyArrow calls the deprecated `__dataframe__` method.
    with tm.assert_produces_warning(match="Interchange", check_stacklevel=False):
        assert pa.Table.equals(pa.interchange.from_dataframe(result), table)

