
def test_ax_legend_set_loc(loc):
    fig, ax = plt.subplots()
    ax.plot(range(10), label='test')
    leg = ax.legend()
    leg.set_loc(loc)
    assert leg._get_loc() == mlegend.Legend.codes[loc]

