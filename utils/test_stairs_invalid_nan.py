
def test_stairs_invalid_nan():
    with pytest.raises(ValueError, match='Nan values in "edges"'):
        plt.stairs([1, 2], [0, np.nan, 1])

