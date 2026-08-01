
def test_axvspan():
    ax = plt.subplot(projection="polar")
    span = ax.axvspan(0, np.pi/4)
    assert span.get_path()._interpolation_steps > 1

