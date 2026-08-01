
def test_color_length_mismatch():
    N = 5
    x, y = np.arange(N), np.arange(N)
    colors = np.arange(N+1)
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        ax.scatter(x, y, c=colors)
    with pytest.warns(match="argument looks like a single numeric RGB"):
        ax.scatter(x, y, c=(0.5, 0.5, 0.5))
    ax.scatter(x, y, c=[(0.5, 0.5, 0.5)] * N)

