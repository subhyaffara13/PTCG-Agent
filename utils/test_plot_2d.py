
def test_plot_2d():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(x, [x, -5, 5, 4], visible=False)
    p.wait_for_calculations()

