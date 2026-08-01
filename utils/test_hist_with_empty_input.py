
def test_hist_with_empty_input(data, expected_number_of_hists):
    hists, _, _ = plt.hist(data)
    hists = np.asarray(hists)

    if hists.ndim == 1:
        assert 1 == expected_number_of_hists
    else:
        assert hists.shape[0] == expected_number_of_hists

