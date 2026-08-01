
def test_non_str_names_w_duplicates():
    # https://github.com/pandas-dev/pandas/issues/56701
    df = pd.DataFrame({"0": [1, 2, 3], 0: [4, 5, 6]})
    with tm.assert_produces_warning(match="Interchange"):
        dfi = df.__dataframe__()
    with tm.assert_produces_warning(match="Interchange"):
        with pytest.raises(
            TypeError,
            match=(
                "Expected a Series, got a DataFrame. This likely happened because you "
                "called __dataframe__ on a DataFrame which, after converting column "
                r"names to string, resulted in duplicated names: Index\(\['0', '0'\], "
                r"dtype='(str|object)'\). Please rename these columns before using the "
                "interchange protocol."
            ),
        ):
            pd.api.interchange.from_dataframe(dfi, allow_copy=False)

