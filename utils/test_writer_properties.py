
def test_writer_properties():
    # Tests getting, setting of properties of matrix writer
    mfw = MatFile5Writer(BytesIO())
    assert_equal(mfw.global_vars, [])
    mfw.global_vars = ['avar']
    assert_equal(mfw.global_vars, ['avar'])
    assert_equal(mfw.unicode_strings, False)
    mfw.unicode_strings = True
    assert_equal(mfw.unicode_strings, True)
    assert_equal(mfw.long_field_names, False)
    mfw.long_field_names = True
    assert_equal(mfw.long_field_names, True)

