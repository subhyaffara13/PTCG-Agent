
def test_plot_integral():
    # Make sure it doesn't treat x as an independent variable
    from sympy.plotting.pygletplot import PygletPlot
    from sympy.integrals.integrals import Integral
    p = PygletPlot(Integral(z*x, (x, 1, z), (z, 1, y)), visible=False)
    p.wait_for_calculations()

