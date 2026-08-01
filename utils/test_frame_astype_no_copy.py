
def test_frame_astype_no_copy():
    # GH 42501
    df = DataFrame({"a": [1, 4, None, 5], "b": [6, 7, 8, 9]}, dtype=object)
    result = df.astype({"a": Int16DtypeNoCopy()})

    assert result.a.dtype == pd.Int16Dtype()
    assert np.shares_memory(df.b.values, result.b.values)

