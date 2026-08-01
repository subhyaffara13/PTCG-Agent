
def _test_plot_log():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(log(x), [x, 0, 6.282, 4], 'mode=polar', visible=False)
    p.wait_for_calculations()

