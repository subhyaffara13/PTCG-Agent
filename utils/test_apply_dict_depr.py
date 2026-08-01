
def test_apply_dict_depr():
    tsdf = DataFrame(
        np.random.default_rng(2).standard_normal((10, 3)),
        columns=["A", "B", "C"],
        index=date_range("1/1/2000", periods=10),
    )
    msg = "nested renamer is not supported"
    with pytest.raises(SpecificationError, match=msg):
        tsdf.A.agg({"foo": ["sum", "mean"]})

