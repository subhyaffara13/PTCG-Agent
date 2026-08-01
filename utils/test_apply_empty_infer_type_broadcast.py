
def test_apply_empty_infer_type_broadcast():
    no_cols = DataFrame(index=["a", "b", "c"])
    result = no_cols.apply(lambda x: x.mean(), result_type="broadcast")
    assert isinstance(result, DataFrame)

