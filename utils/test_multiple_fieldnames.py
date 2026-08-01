
def test_multiple_fieldnames():
    # Example provided by Dharhas Pothina
    # Extracted using mio5.varmats_from_mat
    multi_fname = pjoin(TEST_DATA_PATH, 'nasty_duplicate_fieldnames.mat')
    vars = loadmat(multi_fname)
    funny_names = vars['Summary'].dtype.names
    assert_({'_1_Station_Q', '_2_Station_Q',
                     '_3_Station_Q'}.issubset(funny_names))

