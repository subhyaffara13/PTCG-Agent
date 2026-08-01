
def test_merge_asof_non_numerical_dtype(kwargs, data, infer_string):
    # GH#29130
    with option_context("future.infer_string", infer_string):
        left = pd.DataFrame({"x": data}, index=data)
        right = pd.DataFrame({"x": data}, index=data)
        with pytest.raises(
            MergeError,
            match=r"Incompatible merge dtype, .*, both sides must have numeric dtype",
        ):
            merge_asof(left, right, **kwargs)

