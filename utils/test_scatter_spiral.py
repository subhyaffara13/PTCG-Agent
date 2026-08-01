
def test_scatter_spiral():
    plt.rcParams['axes3d.automargin'] = True  # Remove when image is regenerated
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    th = np.linspace(0, 2 * np.pi * 6, 256)
    sc = ax.scatter(np.sin(th), np.cos(th), th, s=(1 + th * 5), c=th ** 2)

    # force at least 1 draw!
    fig.canvas.draw()

