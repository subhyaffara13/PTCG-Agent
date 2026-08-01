
def test_plot_2d_parametric():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(sin(x), cos(x), [x, 0, 6.282, 4], visible=False)
    p.wait_for_calculations()

