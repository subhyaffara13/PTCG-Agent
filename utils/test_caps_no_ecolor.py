
def test_caps_no_ecolor():

    # Creates a simple plot with error bars without specifying ecolor
    x = np.linspace(0, 10, 10)
    mpl.rcParams['lines.markeredgecolor'] = 'green'
    fig, ax = plt.subplots()
    errorbars = ax.errorbar(x, np.sin(x), yerr=0.1)

    # Tests if the caps have the default color (blue)
    for cap in errorbars[2]:
        assert mcolors.same_color(cap.get_edgecolor(), "blue")

