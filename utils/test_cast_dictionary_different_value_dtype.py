
def test_cast_dictionary_different_value_dtype(arrow_type):
    df = pd.DataFrame({"a": ["x", "y"]}, dtype="string[pyarrow]")
    data_type = ArrowDtype(pa.dictionary(pa.int32(), arrow_type))
    result = df.astype({"a": data_type})
    assert result.dtypes.iloc[0] == data_type

