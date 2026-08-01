
def test_stairs_baseline_None(fig_test, fig_ref):
    x = np.array([0, 2, 3, 5, 10])
    y = np.array([1.148, 1.231, 1.248, 1.25])

    test_axes = fig_test.add_subplot()
    test_axes.stairs(y, x, baseline=None)

    style = {'solid_joinstyle': 'miter', 'solid_capstyle': 'butt'}

    ref_axes = fig_ref.add_subplot()
    ref_axes.plot(x, np.append(y, y[-1]), drawstyle='steps-post', **style)

