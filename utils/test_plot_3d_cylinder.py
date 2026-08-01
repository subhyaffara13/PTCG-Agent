
def test_plot_3d_cylinder():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(
        1/y, [x, 0, 6.282, 4], [y, -1, 1, 4], 'mode=polar;style=solid',
        visible=False)
    p.wait_for_calculations()

