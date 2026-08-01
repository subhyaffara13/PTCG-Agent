
def test_subplot_polar_normalization():
    ax1 = plt.subplot(111, projection='polar')
    ax2 = plt.subplot(111, polar=True)
    ax3 = plt.subplot(111, polar=True, projection='polar')
    assert ax1 is ax2
    assert ax1 is ax3

    with pytest.raises(ValueError,
                       match="polar=True, yet projection='3d'"):
        ax2 = plt.subplot(111, polar=True, projection='3d')

