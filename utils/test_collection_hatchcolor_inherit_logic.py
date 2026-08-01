
def test_collection_hatchcolor_inherit_logic():
    from matplotlib.collections import PathCollection
    path = mpath.Path.unit_rectangle()

    edgecolors = ['purple', 'red', 'green', 'yellow']
    hatchcolors = ['orange', 'cyan', 'blue', 'magenta']
    with mpl.rc_context({'hatch.color': 'edge'}):
        # edgecolor and hatchcolor is set
        col = PathCollection([path], hatch='//',
                              edgecolor=edgecolors, hatchcolor=hatchcolors)
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(hatchcolors))

        # explicitly setting edgecolor and then hatchcolor
        col = PathCollection([path], hatch='//')
        col.set_edgecolor(edgecolors)
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(edgecolors))
        col.set_hatchcolor(hatchcolors)
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(hatchcolors))

        # explicitly setting hatchcolor and then edgecolor
        col = PathCollection([path], hatch='//')
        col.set_hatchcolor(hatchcolors)
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(hatchcolors))
        col.set_edgecolor(edgecolors)
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(hatchcolors))

