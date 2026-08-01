
def test_shares_memory_string():
    # GH#55823
    import pyarrow as pa

    obj = pd.array(["a", "b"], dtype=pd.StringDtype("pyarrow", na_value=pd.NA))
    assert tm.shares_memory(obj, obj)

    obj = pd.array(["a", "b"], dtype=pd.StringDtype("pyarrow", na_value=np.nan))
    assert tm.shares_memory(obj, obj)

    obj = pd.array(["a", "b"], dtype=pd.ArrowDtype(pa.string()))
    assert tm.shares_memory(obj, obj)

