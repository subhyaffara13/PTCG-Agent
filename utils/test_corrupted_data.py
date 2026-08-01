
def test_corrupted_data():
    import zlib
    for exc, fname in [(ValueError, 'corrupted_zlib_data.mat'),
                       (zlib.error, 'corrupted_zlib_checksum.mat')]:
        with open(pjoin(test_data_path, fname), 'rb') as fp:
            rdr = MatFile5Reader(fp)
            assert_raises(exc, rdr.get_variables)

