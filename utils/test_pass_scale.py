
def test_pass_scale():
    # test passing a scale object works...
    fig, ax = plt.subplots()
    scale = mscale.LogScale(axis=None)
    ax.set_xscale(scale)
    scale = mscale.LogScale(axis=None)
    ax.set_yscale(scale)
    assert ax.xaxis.get_scale() == 'log'
    assert ax.yaxis.get_scale() == 'log'

