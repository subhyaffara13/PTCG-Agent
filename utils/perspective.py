
def perspective(fovy, aspect, znear, zfar):
    """
    Build a perspective matrix from field of view, aspect ratio and depth
    planes.

    :param fovy: the field of view angle in the y axis.
    :param aspect: aspect ratio of our view port.
    :param znear: z depth of the near clipping plane.
    :param zfar: z depth of the far clipping plane.

    :return: A perspective matrix.
    """
    h = math.tan(fovy / 360.0 * math.pi) * znear
    w = h * aspect
    return frustum(-w, w, -h, h, znear, zfar)

