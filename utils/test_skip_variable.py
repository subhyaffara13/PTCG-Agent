
def test_skip_variable():
    # Test skipping over the first of two variables in a MAT file
    # using mat_reader_factory and put_variables to read them in.
    #
    # This is a regression test of a problem that's caused by
    # using the compressed file reader seek instead of the raw file
    # I/O seek when skipping over a compressed chunk.
    #
    # The problem arises when the chunk is large: this file has
    # a 256x256 array of random (uncompressible) doubles.
    #
    filename = pjoin(test_data_path,'test_skip_variable.mat')
    #
    # Prove that it loads with loadmat
    #
    d = loadmat(filename, struct_as_record=True)
    assert_('first' in d)
    assert_('second' in d)
    #
    # Make the factory
    #
    factory, file_opened = mat_reader_factory(filename, struct_as_record=True)
    #
    # This is where the factory breaks with an error in MatMatrixGetter.to_next
    #
    d = factory.get_variables('second')
    assert_('second' in d)
    factory.mat_stream.close()

