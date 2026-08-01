
def _sweep_poly_phase(t, poly):
    """
    Calculate the phase used by sweep_poly to generate its output.

    See `sweep_poly` for a description of the arguments.

    """
    # polyint handles lists, ndarrays and instances of poly1d automatically.
    intpoly = polyint(poly)
    phase = 2 * pi * polyval(intpoly, t)
    return phase

