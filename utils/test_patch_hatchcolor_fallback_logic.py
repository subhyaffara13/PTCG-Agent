
def test_patch_hatchcolor_fallback_logic():
    # Test for when hatchcolor parameter is passed
    rect = Rectangle((0, 0), 1, 1, hatch='//', hatchcolor='green')
    assert mcolors.same_color(rect.get_hatchcolor(), 'green')

    # Test that hatchcolor parameter takes precedence over rcParam
    # When edgecolor is not set
    with mpl.rc_context({'hatch.color': 'blue'}):
        rect = Rectangle((0, 0), 1, 1, hatch='//', hatchcolor='green')
    assert mcolors.same_color(rect.get_hatchcolor(), 'green')
    # When edgecolor is set
    with mpl.rc_context({'hatch.color': 'yellow'}):
        rect = Rectangle((0, 0), 1, 1, hatch='//', hatchcolor='green', edgecolor='red')
    assert mcolors.same_color(rect.get_hatchcolor(), 'green')

    # Test that hatchcolor is not overridden by edgecolor when
    # hatchcolor parameter is not passed and hatch.color rcParam is set to a color
    # When edgecolor is not set
    with mpl.rc_context({'hatch.color': 'blue'}):
        rect = Rectangle((0, 0), 1, 1, hatch='//')
    assert mcolors.same_color(rect.get_hatchcolor(), 'blue')
    # When edgecolor is set
    with mpl.rc_context({'hatch.color': 'blue'}):
        rect = Rectangle((0, 0), 1, 1, hatch='//', edgecolor='red')
    assert mcolors.same_color(rect.get_hatchcolor(), 'blue')

    # Test that hatchcolor matches edgecolor when
    # hatchcolor parameter is not passed and hatch.color rcParam is set to 'edge'
    with mpl.rc_context({'hatch.color': 'edge'}):
        rect = Rectangle((0, 0), 1, 1, hatch='//', edgecolor='red')
    assert mcolors.same_color(rect.get_hatchcolor(), 'red')
    # hatchcolor parameter is set to 'edge'
    rect = Rectangle((0, 0), 1, 1, hatch='//', hatchcolor='edge', edgecolor='orange')
    assert mcolors.same_color(rect.get_hatchcolor(), 'orange')

    # Test for default hatchcolor when hatchcolor parameter is not passed and
    # hatch.color rcParam is set to 'edge' and edgecolor is not set
    rect = Rectangle((0, 0), 1, 1, hatch='//')
    assert mcolors.same_color(rect.get_hatchcolor(), mpl.rcParams['patch.edgecolor'])

