
def test_simplify_cells():
    # Test output when simplify_cells=True
    filename = pjoin(test_data_path, 'testsimplecell.mat')
    res1 = loadmat(filename, simplify_cells=True)
    res2 = loadmat(filename, simplify_cells=False)
    assert_(isinstance(res1["s"], dict))
    assert_(isinstance(res2["s"], np.ndarray))
    assert_array_equal(res1["s"]["mycell"], np.array(["a", "b", "c"]))

