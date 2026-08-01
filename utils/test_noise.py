
def test_noise():
    np.random.seed(0)
    x = np.random.uniform(size=50000) * 50

    fig, ax = plt.subplots()
    p1 = ax.plot(x, solid_joinstyle='round', linewidth=2.0)

    # Ensure that the path's transform takes the new axes limits into account.
    fig.canvas.draw()
    path = p1[0].get_path()
    transform = p1[0].get_transform()
    path = transform.transform_path(path)
    simplified = path.cleaned(simplify=True)

    assert simplified.vertices.size == 25512

