
def test_caps_color():

    # Creates a simple plot with error bars and a specified ecolor
    x = np.linspace(0, 10, 10)
    mpl.rcParams['lines.markeredgecolor'] = 'green'
    ecolor = 'red'

    fig, ax = plt.subplots()
    errorbars = ax.errorbar(x, np.sin(x), yerr=0.1, ecolor=ecolor)

    # Tests if the caps have the specified color
    for cap in errorbars[2]:
        assert mcolors.same_color(cap.get_edgecolor(), ecolor)

