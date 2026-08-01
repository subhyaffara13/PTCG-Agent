
def test_set_secondary_axis_color():
    fig, ax = plt.subplots()
    sax = ax.secondary_xaxis("top", color="red")
    assert mcolors.same_color(sax.spines["bottom"].get_edgecolor(), "red")
    assert mcolors.same_color(sax.spines["top"].get_edgecolor(), "red")
    assert mcolors.same_color(sax.xaxis.get_tick_params()["color"], "red")
    assert mcolors.same_color(sax.xaxis.get_tick_params()["labelcolor"], "red")
    assert mcolors.same_color(sax.xaxis.label.get_color(), "red")

