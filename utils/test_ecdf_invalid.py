
def test_ecdf_invalid():
    with pytest.raises(ValueError):
        plt.ecdf([1, np.nan])
    with pytest.raises(ValueError):
        plt.ecdf(np.ma.array([1, 2], mask=[True, False]))

