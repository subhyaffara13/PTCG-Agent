
def test_hatch_colors():
    fig, ax = plt.subplots()
    cf = ax.contourf([[0, 1], [1, 2]], hatches=['-', '/', '\\', '//'], cmap='gray')
    cf.set_edgecolors(["blue", "grey", "yellow", "red"])

