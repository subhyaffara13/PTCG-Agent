
def test_plot_3d_parametric():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(sin(x), cos(x), x/5.0, [x, 0, 6.282, 4], visible=False)
    p.wait_for_calculations()

