
def test_grid_rcparams():
    """Tests that `grid.major/minor.*` overwrites `grid.*` in rcParams."""
    plt.rcParams.update({
        "axes.grid": True, "axes.grid.which": "both",
        "ytick.minor.visible": True, "xtick.minor.visible": True,
    })
    def_linewidth = plt.rcParams["grid.linewidth"]
    def_linestyle = plt.rcParams["grid.linestyle"]
    def_alpha = plt.rcParams["grid.alpha"]

    plt.rcParams.update({
        "grid.color": "gray", "grid.minor.color": "red",
        "grid.major.linestyle": ":", "grid.major.linewidth": 2,
        "grid.minor.alpha": 0.6,
    })
    _, ax = plt.subplots()
    ax.plot([0, 1])

    assert ax.xaxis.get_major_ticks()[0].gridline.get_color() == "gray"
    assert ax.xaxis.get_minor_ticks()[0].gridline.get_color() == "red"
    assert ax.xaxis.get_major_ticks()[0].gridline.get_linewidth() == 2
    assert ax.xaxis.get_minor_ticks()[0].gridline.get_linewidth() == def_linewidth
    assert ax.xaxis.get_major_ticks()[0].gridline.get_linestyle() == ":"
    assert ax.xaxis.get_minor_ticks()[0].gridline.get_linestyle() == def_linestyle
    assert ax.xaxis.get_major_ticks()[0].gridline.get_alpha() == def_alpha
    assert ax.xaxis.get_minor_ticks()[0].gridline.get_alpha() == 0.6

