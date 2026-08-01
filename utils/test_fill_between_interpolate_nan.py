
def test_fill_between_interpolate_nan():
    # Tests fix for issue #18986.
    x = np.arange(10)
    y1 = np.asarray([8, 18, np.nan, 18, 8, 18, 24, 18, 8, 18])
    y2 = np.asarray([18, 11, 8, 11, 18, 26, 32, 30, np.nan, np.nan])

    fig, ax = plt.subplots()

    ax.plot(x, y1, c='k')
    ax.plot(x, y2, c='b')
    ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor="green",
                    interpolate=True, alpha=0.5)
    ax.fill_between(x, y1, y2, where=y1 >= y2, facecolor="red",
                    interpolate=True, alpha=0.5)

