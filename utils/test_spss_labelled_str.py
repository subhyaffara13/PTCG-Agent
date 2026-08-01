
def test_spss_labelled_str(datapath):
    # test file from the Haven project (https://haven.tidyverse.org/)
    # Licence at LICENSES/HAVEN_LICENSE, LICENSES/HAVEN_MIT
    fname = datapath("io", "data", "spss", "labelled-str.sav")

    df = pd.read_spss(fname, convert_categoricals=True)
    expected = pd.DataFrame({"gender": ["Male", "Female"]})
    expected["gender"] = pd.Categorical(expected["gender"])
    tm.assert_frame_equal(df, expected)

    df = pd.read_spss(fname, convert_categoricals=False)
    expected = pd.DataFrame({"gender": ["M", "F"]})
    tm.assert_frame_equal(df, expected)

