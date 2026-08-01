
def transverse_magnification(si, so):
    """

    Calculates the transverse magnification upon reflection in a mirror,
    which is the ratio of the image size to the object size.

    Parameters
    ==========

    so: sympifiable
        Lens-object distance.

    si: sympifiable
        Lens-image distance.

    Example
    =======

    >>> from sympy.physics.optics import transverse_magnification
    >>> transverse_magnification(30, 15)
    -2

    """

    si = sympify(si)
    so = sympify(so)

    return (-(si/so))

