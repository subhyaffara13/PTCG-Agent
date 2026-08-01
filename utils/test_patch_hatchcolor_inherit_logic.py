
def test_patch_hatchcolor_inherit_logic():
    with mpl.rc_context({'hatch.color': 'edge'}):
        # Test for when edgecolor and hatchcolor is set
        rect = Rectangle((0, 0), 1, 1, hatch='//', ec='red',
                         hatchcolor='yellow')
        assert mcolors.same_color(rect.get_edgecolor(), 'red')
        assert mcolors.same_color(rect.get_hatchcolor(), 'yellow')

        # Test for explicitly setting edgecolor and then hatchcolor
        rect = Rectangle((0, 0), 1, 1, hatch='//')
        rect.set_edgecolor('orange')
        assert mcolors.same_color(rect.get_hatchcolor(), 'orange')
        rect.set_hatchcolor('cyan')
        assert mcolors.same_color(rect.get_hatchcolor(), 'cyan')

        # Test for explicitly setting hatchcolor and then edgecolor
        rect = Rectangle((0, 0), 1, 1, hatch='//')
        rect.set_hatchcolor('purple')
        assert mcolors.same_color(rect.get_hatchcolor(), 'purple')
        rect.set_edgecolor('green')
        assert mcolors.same_color(rect.get_hatchcolor(), 'purple')

    # Smoke test for setting with numpy array
    rect.set_hatchcolor(np.ones(3))

