
def test_legend_auto1():
    """Test automatic legend placement"""
    fig, ax = plt.subplots()
    x = np.arange(100)
    ax.plot(x, 50 - x, 'o', label='y=1')
    ax.plot(x, x - 50, 'o', label='y=-1')
    ax.legend(loc='best')

