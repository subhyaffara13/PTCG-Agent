
def test_spss_umlauts_dtype_backend(datapath, dtype_backend):
    # test file from the Haven project (https://haven.tidyverse.org/)
    # Licence at LICENSES/HAVEN_LICENSE, LICENSES/HAVEN_MIT
    fname = datapath("io", "data", "spss", "umlauts.sav")

    df = pd.read_spss(fname, convert_categoricals=False, dtype_backend=dtype_backend)
    expected = pd.DataFrame({"var1": [1.0, 2.0, 1.0, 3.0]}, dtype="Int64")

    if dtype_backend == "pyarrow":
        pa = pytest.importorskip("pyarrow")

        from pandas.arrays import ArrowExtensionArray

        expected = pd.DataFrame(
            {
                col: ArrowExtensionArray(pa.array(expected[col], from_pandas=True))
                for col in expected.columns
            }
        )

    tm.assert_frame_equal(df, expected)

