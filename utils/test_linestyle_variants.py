
def test_linestyle_variants():
    fig, ax = plt.subplots()
    for ls in ["-", "solid", "--", "dashed",
               "-.", "dashdot", ":", "dotted",
               (0, None), (0, ()), (0, []),  # gh-22930
               ]:
        ax.plot(range(10), linestyle=ls)
    fig.canvas.draw()

