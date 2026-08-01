
def test_not_covering_scatter_transform():
    # Offsets point to top left, the default auto position
    offset = mtransforms.Affine2D().translate(-20, 20)
    x = np.linspace(0, 30, 1000)
    plt.plot(x, x)

    plt.scatter([20], [10], transform=offset + plt.gca().transData)

    plt.legend(['foo', 'bar'], loc='best')

