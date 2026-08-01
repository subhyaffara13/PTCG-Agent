
def test_4_and_long_field_names_incompatible():
    # Long field names option not supported in 4
    my_struct = np.zeros((1,1),dtype=[('my_fieldname',object)])
    assert_raises(ValueError, savemat, BytesIO(),
                  {'my_struct':my_struct}, format='4', long_field_names=True)

