
def test_aitoff_proj():
    """
    Test aitoff projection ref.:
    https://github.com/matplotlib/matplotlib/pull/14451
    """
    x = np.linspace(-np.pi, np.pi, 20)
    y = np.linspace(-np.pi / 2, np.pi / 2, 20)
    X, Y = np.meshgrid(x, y)

    fig, ax = plt.subplots(figsize=(8, 4.2),
                           subplot_kw=dict(projection="aitoff"))
    ax.grid()
    ax.plot(X.flat, Y.flat, 'o', markersize=4)

