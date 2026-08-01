
def test_column_get_chunks(size, n_chunks, df_from_dict):
    df = df_from_dict({"x": list(range(size))})
    with tm.assert_produces_warning(match="Interchange"):
        dfX = df.__dataframe__()
    chunks = list(dfX.get_column(0).get_chunks(n_chunks))
    assert len(chunks) == n_chunks
    assert sum(chunk.size() for chunk in chunks) == size

