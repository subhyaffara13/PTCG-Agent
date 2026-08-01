
def test_collection_hatchcolor_fallback_logic():
    from matplotlib.collections import PathCollection
    path = mpath.Path.unit_rectangle()

    edgecolors = ['purple', 'red', 'green', 'yellow']
    hatchcolors = ['orange', 'cyan', 'blue', 'magenta']

    # hatchcolor parameter should take precedence over rcParam
    # When edgecolor is not set
    with mpl.rc_context({'hatch.color': 'green'}):
        col = PathCollection([path], hatch='//', hatchcolor=hatchcolors)
    assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(hatchcolors))
    # When edgecolor is set
    with mpl.rc_context({'hatch.color': 'green'}):
        col = PathCollection([path], hatch='//',
                             edgecolor=edgecolors, hatchcolor=hatchcolors)
    assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(hatchcolors))

    # hatchcolor should not be overridden by edgecolor when
    # hatchcolor parameter is not passed and hatch.color rcParam is set to a color
    with mpl.rc_context({'hatch.color': 'green'}):
        col = PathCollection([path], hatch='//')
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array('green'))
        col.set_edgecolor(edgecolors)
        assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array('green'))

    # hatchcolor should match edgecolor when
    # hatchcolor parameter is not passed and hatch.color rcParam is set to 'edge'
    with mpl.rc_context({'hatch.color': 'edge'}):
        col = PathCollection([path], hatch='//', edgecolor=edgecolors)
    assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(edgecolors))
    # hatchcolor parameter is set to 'edge'
    col = PathCollection([path], hatch='//', edgecolor=edgecolors, hatchcolor='edge')
    assert_array_equal(col.get_hatchcolor(), mpl.colors.to_rgba_array(edgecolors))

    # default hatchcolor should be used when hatchcolor parameter is not passed and
    # hatch.color rcParam is set to 'edge' and edgecolor is not set
    col = PathCollection([path], hatch='//')
    assert_array_equal(col.get_hatchcolor(),
                       mpl.colors.to_rgba_array(mpl.rcParams['patch.edgecolor']))

