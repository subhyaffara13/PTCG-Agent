
def test_date_not_empty():
    fig = plt.figure()
    ax = fig.add_subplot()

    ax.plot([50, 70], [1, 2])
    ax.xaxis.axis_date()
    np.testing.assert_allclose(ax.get_xlim(), [50, 70])

