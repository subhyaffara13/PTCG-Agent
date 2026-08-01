
def create_figure():
    plt.figure()
    x = np.linspace(0, 1, 15)

    # line plot
    plt.plot(x, x ** 2, "b-")

    # marker
    plt.plot(x, 1 - x**2, "g>")

    # filled paths and patterns
    plt.fill_between([0., .4], [.4, 0.], hatch='//', facecolor="lightgray",
                     edgecolor="red")
    plt.fill([3, 3, .8, .8, 3], [2, -2, -2, 0, 2], "b")

    # text and typesetting
    plt.plot([0.9], [0.5], "ro", markersize=3)
    plt.text(0.9, 0.5, 'unicode (ü, °, \N{Section Sign}) and math ($\\mu_i = x_i^2$)',
             ha='right', fontsize=20)
    plt.ylabel('sans-serif, blue, $\\frac{\\sqrt{x}}{y^2}$..',
               family='sans-serif', color='blue')
    plt.text(1, 1, 'should be clipped as default clip_box is Axes bbox',
             fontsize=20, clip_on=True)

    plt.xlim(0, 1)
    plt.ylim(0, 1)

