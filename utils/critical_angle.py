
def critical_angle(medium1, medium2):
    """
    This function calculates the critical angle of incidence (marking the onset
    of total internal) to Medium 2 from Medium 1 in radians.

    Parameters
    ==========

    medium 1 : Medium or sympifiable
        Refractive index of Medium 1.
    medium 2 : Medium or sympifiable
        Refractive index of Medium 1.

    Examples
    ========

    >>> from sympy.physics.optics import critical_angle
    >>> critical_angle(1.33, 1)
    0.850908514477849

    """

    n1 = refractive_index_of_medium(medium1)
    n2 = refractive_index_of_medium(medium2)

    if n2 > n1:
        raise ValueError('Total internal reflection impossible for n1 < n2')
    else:
        return asin(n2/n1)

