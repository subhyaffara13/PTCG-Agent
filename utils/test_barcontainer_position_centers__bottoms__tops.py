
def test_barcontainer_position_centers__bottoms__tops():
    fig, ax = plt.subplots()
    pos = [1, 2, 4]
    bottoms = np.array([1, 5, 3])
    heights = np.array([2, 3, 4])

    container = ax.bar(pos, heights, bottom=bottoms)
    assert_array_equal(container.position_centers, pos)
    assert_array_equal(container.bottoms, bottoms)
    assert_array_equal(container.tops, bottoms + heights)

    container = ax.barh(pos, heights, left=bottoms)
    assert_array_equal(container.position_centers, pos)
    assert_array_equal(container.bottoms, bottoms)
    assert_array_equal(container.tops, bottoms + heights)

