
def test_long_field_names_in_struct():
    # Regression test - long_field_names was erased if you passed a struct
    # within a struct
    lim = 63
    fldname = 'a' * lim
    cell = np.ndarray((1,2),dtype=object)
    st1 = np.zeros((1,1), dtype=[(fldname, object)])
    cell[0,0] = st1
    cell[0,1] = st1
    savemat(BytesIO(), {'longstruct': cell}, format='5',long_field_names=True)
    #
    # Check to make sure it fails with long field names off
    #
    assert_raises(ValueError, savemat, BytesIO(),
                  {'longstruct': cell}, format='5', long_field_names=False)

