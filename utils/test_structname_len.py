
def test_structname_len():
    # Test limit for length of field names in structs
    lim = 31
    fldname = 'a' * lim
    st1 = np.zeros((1,1), dtype=[(fldname, object)])
    savemat(BytesIO(), {'longstruct': st1}, format='5')
    fldname = 'a' * (lim+1)
    st1 = np.zeros((1,1), dtype=[(fldname, object)])
    assert_raises(ValueError, savemat, BytesIO(),
                  {'longstruct': st1}, format='5')

