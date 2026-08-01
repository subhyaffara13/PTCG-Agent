
def test_dtype_equality():
    pytest.importorskip("pyarrow")

    dtype1 = pd.StringDtype("python")
    dtype2 = pd.StringDtype("pyarrow")
    dtype3 = pd.StringDtype("pyarrow", na_value=np.nan)

    assert dtype1 == pd.StringDtype("python", na_value=pd.NA)
    assert dtype1 != dtype2
    assert dtype1 != dtype3

    assert dtype2 == pd.StringDtype("pyarrow", na_value=pd.NA)
    assert dtype2 != dtype1
    assert dtype2 != dtype3

    assert dtype3 == pd.StringDtype("pyarrow", na_value=np.nan)
    assert dtype3 == pd.StringDtype("pyarrow", na_value=float("nan"))
    assert dtype3 != dtype1
    assert dtype3 != dtype2


def test_dtype_equality(dtype):
    assert dtype == dtype
    for ch in "SU":
        assert dtype != np.dtype(ch)
        assert dtype != np.dtype(f"{ch}8")

