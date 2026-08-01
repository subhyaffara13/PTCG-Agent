
def test_stairs_invalid_update2():
    h = plt.stairs([1, 2], [0, 1, 2])
    with pytest.raises(ValueError, match='Size mismatch'):
        h.set_data(edges=np.arange(5))

