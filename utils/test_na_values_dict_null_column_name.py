
def test_na_values_dict_null_column_name(all_parsers):
    # see gh-57547
    parser = all_parsers
    data = ",x,y\n\nMA,1,2\nNA,2,1\nOA,,3"
    names = [None, "x", "y"]
    na_values = dict.fromkeys(names, STR_NA_VALUES)
    dtype = {None: "object", "x": "float64", "y": "float64"}

    if parser.engine == "pyarrow":
        msg = "The pyarrow engine doesn't support passing a dict for na_values"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data),
                index_col=0,
                header=0,
                dtype=dtype,
                names=names,
                na_values=na_values,
                keep_default_na=False,
            )
        return

    expected = DataFrame(
        {"x": [1.0, 2.0, np.nan], "y": [2.0, 1.0, 3.0]},
        index=Index(["MA", "NA", "OA"], dtype=object),
    )

    result = parser.read_csv(
        StringIO(data),
        index_col=0,
        header=0,
        dtype=dtype,
        names=names,
        na_values=na_values,
        keep_default_na=False,
    )

    tm.assert_frame_equal(result, expected)

