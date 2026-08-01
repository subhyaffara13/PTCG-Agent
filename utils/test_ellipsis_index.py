
def test_ellipsis_index():
    # GH#42430 1D slices over extension types turn into N-dimensional slices
    #  over ExtensionArrays
    dtype = pd.StringDtype()
    df = pd.DataFrame(
        {
            "col1": CapturingStringArray(
                np.array(["hello", "world"], dtype=object), dtype=dtype
            )
        }
    )
    _ = df.iloc[:1]

    # String comparison because there's no native way to compare slices.
    # Before the fix for GH#42430, last_item_arg would get set to the 2D slice
    # (Ellipsis, slice(None, 1, None))
    out = df["col1"]._values.last_item_arg
    assert str(out) == "slice(None, 1, None)"

