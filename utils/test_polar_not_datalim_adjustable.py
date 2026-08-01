
def test_polar_not_datalim_adjustable():
    ax = plt.figure().add_subplot(projection="polar")
    with pytest.raises(ValueError):
        ax.set_adjustable("datalim")

