
def test_logscale_transform_repr():
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    repr(ax.transData)
    repr(LogTransform(10, nonpositive='clip'))

