
def test_bitmasks_pyarrow(offset, length, expected_values):
    # GH 52795
    pa = pytest.importorskip("pyarrow", "11.0.0")

    arr = [3.3, None, 2.1]
    table = pa.table({"arr": arr}).slice(offset, length)
    exchange_df = table.__dataframe__()
    with tm.assert_produces_warning(match="Interchange"):
        result = from_dataframe(exchange_df)
    expected = pd.DataFrame({"arr": expected_values})
    tm.assert_frame_equal(result, expected)

    # check round-trip
    # Don't check stacklevel as PyArrow calls the deprecated `__dataframe__` method.
    with tm.assert_produces_warning(match="Interchange", check_stacklevel=False):
        assert pa.Table.equals(pa.interchange.from_dataframe(result), table)

