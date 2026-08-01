
def test_plot_3d_discontinuous():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(1/x, [x, -3, 3, 6], [y, -1, 1, 1], visible=False)
    p.wait_for_calculations()

