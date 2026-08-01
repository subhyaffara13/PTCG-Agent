
def test_thetalim_args():
    ax = plt.subplot(projection='polar')
    ax.set_thetalim(0, 1)
    assert tuple(np.radians((ax.get_thetamin(), ax.get_thetamax()))) == (0, 1)
    ax.set_thetalim((2, 3))
    assert tuple(np.radians((ax.get_thetamin(), ax.get_thetamax()))) == (2, 3)

