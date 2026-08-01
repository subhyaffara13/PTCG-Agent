
def plot_polytope(poly):
    """Plots the 2D polytope using the functions written in plotting
    module which in turn uses matplotlib backend.

    Parameter
    =========

    poly:
        Denotes a 2-Polytope.
    """
    from sympy.plotting.plot import Plot, List2DSeries

    xl = [vertex.x for vertex in poly.vertices]
    yl = [vertex.y for vertex in poly.vertices]

    xl.append(poly.vertices[0].x)  # Closing the polygon
    yl.append(poly.vertices[0].y)

    l2ds = List2DSeries(xl, yl)
    p = Plot(l2ds, axes='label_axes=True')
    p.show()

