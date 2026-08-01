
def test_spss_kwargs(datapath):
    # test file from the Haven project (https://haven.tidyverse.org/)
    # Licence at LICENSES/HAVEN_LICENSE, LICENSES/HAVEN_MIT
    fname = datapath("io", "data", "spss", "labelled-str.sav")

    df = pd.read_spss(fname, convert_categoricals=True, row_limit=1)
    expected = pd.DataFrame({"gender": ["Male"]}, dtype="category")
    tm.assert_frame_equal(df, expected)

    df = pd.read_spss(fname, convert_categoricals=False, row_offset=1)
    expected = pd.DataFrame({"gender": ["F"]})
    tm.assert_frame_equal(df, expected)

