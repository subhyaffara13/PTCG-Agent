
def test_astype_nansafe():
    # see gh-22343
    arr = pd.array([pd.NA, 1, 2], dtype="Int8")
    msg = "cannot convert NA to integer"

    with pytest.raises(ValueError, match=msg):
        arr.astype("uint32")

