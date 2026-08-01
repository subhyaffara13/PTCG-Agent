
def test_nan_isolated_points():

    y0 = [0, np.nan, 2, np.nan, 4, 5, 6]
    y1 = [np.nan, 7, np.nan, 9, 10, np.nan, 12]

    fig, ax = plt.subplots()

    ax.plot(y0, '-o')
    ax.plot(y1, '-o')

