
def test_plot_3d_spherical():
    from sympy.plotting.pygletplot import PygletPlot
    p = PygletPlot(
        1, [x, 0, 6.282, 4], [y, 0, 3.141,
            4], 'mode=spherical;style=wireframe',
        visible=False)
    p.wait_for_calculations()

