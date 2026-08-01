
def test_plotting2():
    #from sympy.plotting.color_scheme import ColorGradient
    from sympy.plotting.pygletplot.color_scheme import ColorScheme
    #from sympy.plotting.managed_window import ManagedWindow
    from sympy.plotting.plot import Plot
    #from sympy.plotting.plot import ScreenShot
    from sympy.plotting.pygletplot.plot_axes import PlotAxes
    #from sympy.plotting.plot_axes import PlotAxesBase, PlotAxesFrame, PlotAxesOrdinate
    #from sympy.plotting.plot_camera import PlotCamera
    #from sympy.plotting.plot_controller import PlotController
    #from sympy.plotting.plot_curve import PlotCurve
    #from sympy.plotting.plot_interval import PlotInterval
    #from sympy.plotting.plot_mode import PlotMode
    #from sympy.plotting.plot_modes import Cartesian2D, Cartesian3D, Cylindrical, \
    #    ParametricCurve2D, ParametricCurve3D, ParametricSurface, Polar, Spherical
    #from sympy.plotting.plot_object import PlotObject
    #from sympy.plotting.plot_surface import PlotSurface
    # from sympy.plotting.plot_window import PlotWindow
    check(ColorScheme("rainbow"))
    check(Plot(1, visible=False))
    check(PlotAxes())

