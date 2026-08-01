
def test_stairs_invalid_mismatch():
    with pytest.raises(ValueError, match='Size mismatch'):
        plt.stairs([1, 2], [0, 1])

