
def test_facecolor_none_edgecolor_force_edgecolor():

    # Case 1:force_edgecolor =False -> rcParams['patch.edgecolor'] should NOT be applied
    rcParams['patch.force_edgecolor'] = False
    rcParams['patch.edgecolor'] = 'red'
    rect = Rectangle((0, 0), 1, 1, facecolor="none")
    assert not mcolors.same_color(rect.get_edgecolor(), rcParams['patch.edgecolor'])

    # Case 2:force_edgecolor =True -> rcParams['patch.edgecolor'] SHOULD be applied
    rcParams['patch.force_edgecolor'] = True
    rcParams['patch.edgecolor'] = 'red'
    rect = Rectangle((0, 0), 1, 1, facecolor="none")
    assert mcolors.same_color(rect.get_edgecolor(), rcParams['patch.edgecolor'])

