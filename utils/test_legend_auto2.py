
def test_legend_auto2():
    """Test automatic legend placement"""
    fig, ax = plt.subplots()
    x = np.arange(100)
    b1 = ax.bar(x, x, align='edge', color='m')
    b2 = ax.bar(x, x[::-1], align='edge', color='g')
    ax.legend([b1[0], b2[0]], ['up', 'down'], loc='best')

