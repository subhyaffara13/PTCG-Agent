
def test_fig_legend_set_loc(loc):
    fig, ax = plt.subplots()
    ax.plot(range(10), label='test')
    leg = fig.legend()
    leg.set_loc(loc)

    loc = loc.split()[1] if loc.startswith("outside") else loc
    assert leg._get_loc() == mlegend.Legend.codes[loc]

