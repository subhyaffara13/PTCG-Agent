
def test_removal():
    import matplotlib.pyplot as plt
    import mpl_toolkits.axisartist as AA
    fig = plt.figure()
    ax = host_subplot(111, axes_class=AA.Axes, figure=fig)
    col = ax.fill_between(range(5), 0, range(5))
    fig.canvas.draw()
    col.remove()
    fig.canvas.draw()

