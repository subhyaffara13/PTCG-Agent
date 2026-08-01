
def test_plotting():
    from sympy.plotting.pygletplot.color_scheme import ColorGradient, ColorScheme
    from sympy.plotting.pygletplot.managed_window import ManagedWindow
    from sympy.plotting.plot import Plot, ScreenShot
    from sympy.plotting.pygletplot.plot_axes import PlotAxes, PlotAxesBase, PlotAxesFrame, PlotAxesOrdinate
    from sympy.plotting.pygletplot.plot_camera import PlotCamera
    from sympy.plotting.pygletplot.plot_controller import PlotController
    from sympy.plotting.pygletplot.plot_curve import PlotCurve
    from sympy.plotting.pygletplot.plot_interval import PlotInterval
    from sympy.plotting.pygletplot.plot_mode import PlotMode
    from sympy.plotting.pygletplot.plot_modes import Cartesian2D, Cartesian3D, Cylindrical, \
        ParametricCurve2D, ParametricCurve3D, ParametricSurface, Polar, Spherical
    from sympy.plotting.pygletplot.plot_object import PlotObject
    from sympy.plotting.pygletplot.plot_surface import PlotSurface
    from sympy.plotting.pygletplot.plot_window import PlotWindow
    for c in (
        ColorGradient, ColorGradient(0.2, 0.4), ColorScheme, ManagedWindow,
        ManagedWindow, Plot, ScreenShot, PlotAxes, PlotAxesBase,
        PlotAxesFrame, PlotAxesOrdinate, PlotCamera, PlotController,
        PlotCurve, PlotInterval, PlotMode, Cartesian2D, Cartesian3D,
        Cylindrical, ParametricCurve2D, ParametricCurve3D,
        ParametricSurface, Polar, Spherical, PlotObject, PlotSurface,
            PlotWindow):
        check(c)

