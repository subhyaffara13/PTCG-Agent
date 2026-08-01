
def test_subplot_kwarg_collision():
    ax1 = plt.subplot(projection='polar', theta_offset=0)
    ax2 = plt.subplot(projection='polar', theta_offset=0)
    assert ax1 is ax2
    ax1.remove()
    ax3 = plt.subplot(projection='polar', theta_offset=1)
    assert ax1 is not ax3
    assert ax1 not in plt.gcf().axes

