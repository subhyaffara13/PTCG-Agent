
def _rot(axis, angle):
    """DCM for simple axis 1, 2 or 3 rotations. """
    if axis == 1:
        return Matrix(rot_axis1(angle).T)
    elif axis == 2:
        return Matrix(rot_axis2(angle).T)
    elif axis == 3:
        return Matrix(rot_axis3(angle).T)

