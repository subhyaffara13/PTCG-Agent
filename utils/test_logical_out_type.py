
def test_logical_out_type():
    # Confirm that bool type written as uint8, uint8 class
    # See gh-4022
    stream = BytesIO()
    barr = np.array([False, True, False])
    savemat(stream, {'barray': barr})
    stream.seek(0)
    reader = MatFile5Reader(stream)
    reader.initialize_read()
    reader.read_file_header()
    hdr, _ = reader.read_var_header()
    assert_equal(hdr.mclass, mio5p.mxUINT8_CLASS)
    assert_equal(hdr.is_logical, True)
    var = reader.read_var_array(hdr, False)
    assert_equal(var.dtype.type, np.uint8)

