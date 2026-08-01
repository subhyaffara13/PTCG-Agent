
def test_min_max_full():
    for a in (coo_array([[[1, 2, 3, 4]]]), coo_array([[1, 2, 3, 4]])):
        assert a.min() == 1
        assert (-a).max() == -1

