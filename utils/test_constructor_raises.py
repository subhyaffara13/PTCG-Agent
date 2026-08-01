
def test_constructor_raises(cls):
    if cls is pd.arrays.StringArray:
        msg = "StringArray requires a sequence of strings or pandas.NA"
        kwargs = {"dtype": pd.StringDtype()}
    else:
        msg = "Unsupported type '<class 'numpy.ndarray'>' for ArrowExtensionArray"
        kwargs = {}

    with pytest.raises(ValueError, match=msg):
        cls(np.array(["a", "b"], dtype="S1"), **kwargs)

    with pytest.raises(ValueError, match=msg):
        cls(np.array([]), **kwargs)

    if cls is pd.arrays.StringArray:
        # GH#45057 np.nan and None do NOT raise, as they are considered valid NAs
        #  for string dtype
        cls(np.array(["a", np.nan], dtype=object), **kwargs)
        cls(np.array(["a", None], dtype=object), **kwargs)
    else:
        with pytest.raises(ValueError, match=msg):
            cls(np.array(["a", np.nan], dtype=object), **kwargs)
        with pytest.raises(ValueError, match=msg):
            cls(np.array(["a", None], dtype=object), **kwargs)

    with pytest.raises(ValueError, match=msg):
        cls(np.array(["a", pd.NaT], dtype=object), **kwargs)

    with pytest.raises(ValueError, match=msg):
        cls(np.array(["a", np.datetime64("NaT", "ns")], dtype=object), **kwargs)

    with pytest.raises(ValueError, match=msg):
        cls(np.array(["a", np.timedelta64("NaT", "ns")], dtype=object), **kwargs)

