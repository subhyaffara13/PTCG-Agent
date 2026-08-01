
def test_strl_missings(temp_file, version):
    # GH 23633
    # Check that strl supports None and pd.NA
    df = DataFrame(
        [
            {"str1": "string" * 500, "number": 0},
            {"str1": None, "number": 1},
            {"str1": pd.NA, "number": 1},
        ]
    )
    df.to_stata(temp_file, version=version)

