
def test_gh_17992(tmp_path):
    rng = np.random.default_rng(12345)
    outfile = tmp_path / "lists.mat"
    array_one = rng.random((5,3))
    array_two = rng.random((6,3))
    list_of_arrays = [array_one, array_two]
    savemat(outfile,
            {'data': list_of_arrays},
            long_field_names=True,
            do_compression=True)
    # round trip check
    new_dict = {}
    loadmat(outfile,
            new_dict)
    assert_allclose(new_dict["data"][0][0], array_one)
    assert_allclose(new_dict["data"][0][1], array_two)

