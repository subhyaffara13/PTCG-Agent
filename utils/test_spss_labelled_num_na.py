
def test_spss_labelled_num_na(datapath):
    # test file from the Haven project (https://haven.tidyverse.org/)
    # Licence at LICENSES/HAVEN_LICENSE, LICENSES/HAVEN_MIT
    fname = datapath("io", "data", "spss", "labelled-num-na.sav")

    df = pd.read_spss(fname, convert_categoricals=True)
    expected = pd.DataFrame({"VAR00002": ["This is one", None]})
    expected["VAR00002"] = pd.Categorical(expected["VAR00002"])
    tm.assert_frame_equal(df, expected)

    df = pd.read_spss(fname, convert_categoricals=False)
    expected = pd.DataFrame({"VAR00002": [1.0, np.nan]})
    tm.assert_frame_equal(df, expected)

