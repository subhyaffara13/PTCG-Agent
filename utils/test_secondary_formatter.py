
def test_secondary_formatter():
    fig, ax = plt.subplots()
    ax.set_xscale("log")
    secax = ax.secondary_xaxis("top")
    secax.xaxis.set_major_formatter(mticker.ScalarFormatter())
    fig.canvas.draw()
    assert isinstance(
        secax.xaxis.get_major_formatter(), mticker.ScalarFormatter)

