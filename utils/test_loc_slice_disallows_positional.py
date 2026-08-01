
def test_loc_slice_disallows_positional():
    # GH#16121, GH#24612, GH#31810
    dti = date_range("2016-01-01", periods=3)
    df = DataFrame(np.random.default_rng(2).random((3, 2)), index=dti)

    ser = df[0]

    msg = (
        "cannot do slice indexing on DatetimeIndex with these "
        r"indexers \[1\] of type int"
    )

    for obj in [df, ser]:
        with pytest.raises(TypeError, match=msg):
            obj.loc[1:3]

        with pytest.raises(TypeError, match="Slicing a positional slice with .loc"):
            # GH#31840 enforce incorrect behavior
            obj.loc[1:3] = 1

    with pytest.raises(TypeError, match=msg):
        df.loc[1:3, 1]

    with pytest.raises(TypeError, match="Slicing a positional slice with .loc"):
        # GH#31840 enforce incorrect behavior
        df.loc[1:3, 1] = 2

