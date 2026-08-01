
def test_long_field_names():
    # Test limit for length of field names in structs
    lim = 63
    fldname = 'a' * lim
    st1 = np.zeros((1,1), dtype=[(fldname, object)])
    savemat(BytesIO(), {'longstruct': st1}, format='5',long_field_names=True)
    fldname = 'a' * (lim+1)
    st1 = np.zeros((1,1), dtype=[(fldname, object)])
    assert_raises(ValueError, savemat, BytesIO(),
                  {'longstruct': st1}, format='5',long_field_names=True)

