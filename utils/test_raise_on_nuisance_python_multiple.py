
def test_raise_on_nuisance_python_multiple(three_group, using_infer_string):
    grouped = three_group.groupby(["A", "B"])
    msg = re.escape("agg function failed [how->mean,dtype->")
    if using_infer_string:
        msg = "dtype 'str' does not support operation 'mean'"
    with pytest.raises(TypeError, match=msg):
        grouped.agg("mean")
    with pytest.raises(TypeError, match=msg):
        grouped.mean()

