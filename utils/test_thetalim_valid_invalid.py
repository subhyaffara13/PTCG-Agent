
def test_thetalim_valid_invalid():
    ax = plt.subplot(projection='polar')
    ax.set_thetalim(0, 2 * np.pi)  # doesn't raise.
    ax.set_thetalim(thetamin=800, thetamax=440)  # doesn't raise.
    with pytest.raises(ValueError,
                       match='angle range must be less than a full circle'):
        ax.set_thetalim(0, 3 * np.pi)
    with pytest.raises(ValueError,
                       match='angle range must be less than a full circle'):
        ax.set_thetalim(thetamin=800, thetamax=400)

