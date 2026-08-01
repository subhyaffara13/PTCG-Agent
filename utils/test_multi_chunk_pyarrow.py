
def test_multi_chunk_pyarrow() -> None:
    pa = pytest.importorskip("pyarrow", "14.0.0")
    n_legs = pa.chunked_array([[2, 2, 4], [4, 5, 100]])
    names = ["n_legs"]
    table = pa.table([n_legs], names=names)
    with pytest.raises(
        RuntimeError,
        match="Cannot do zero copy conversion into multi-column DataFrame block",
    ):
        pd.api.interchange.from_dataframe(table, allow_copy=False)

