
def test_autoscale_tiny_sticky():
    fig, ax = plt.subplots()
    ax.bar(0, 1e-9)
    fig.canvas.draw()
    assert ax.get_ylim() == (0, 1.05e-9)

