
def test_blended_collection_autolim():
    f, ax = plt.subplots()

    # sample data to give initial data limits
    ax.plot([2, 3, 4], [0.4, 0.6, 0.5])
    np.testing.assert_allclose((ax.dataLim.xmin, ax.dataLim.xmax), (2, 4))
    data_ymin, data_ymax = ax.dataLim.ymin, ax.dataLim.ymax

    # LineCollection with vertical lines spanning the Axes vertical, using transAxes
    x = [1, 2, 3, 4, 5]
    vertical_lines = [np.array([[xi, 0], [xi, 1]]) for xi in x]
    trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    ax.add_collection(LineCollection(vertical_lines, transform=trans))

    # check that the x data limits are updated to include the LineCollection
    np.testing.assert_allclose((ax.dataLim.xmin, ax.dataLim.xmax), (1, 5))
    # check that the y data limits are not updated (because they are not transData)
    np.testing.assert_allclose((ax.dataLim.ymin, ax.dataLim.ymax),
                               (data_ymin, data_ymax))

