
def test_corrupted_data_check_can_be_disabled():
    with open(pjoin(test_data_path, 'corrupted_zlib_data.mat'), 'rb') as fp:
        rdr = MatFile5Reader(fp, verify_compressed_data_integrity=False)
        rdr.get_variables()

