
def test_converters_dict_raises_non_col_key(bad_col_ind):
    data = StringIO("1 2\n3 4")
    with pytest.raises(ValueError, match="converter specified for column"):
        np.loadtxt(data, converters={bad_col_ind: int})

