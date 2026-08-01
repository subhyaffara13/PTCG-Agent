
def test_legend_nolabels_warning():
    plt.plot([1, 2, 3])
    with pytest.raises(UserWarning, match="No artists with labels found"):
        plt.legend()

