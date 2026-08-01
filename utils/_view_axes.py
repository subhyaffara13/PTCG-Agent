
def _view_axes(E, R, V, roll):
    """
    Get the unit viewing axes in data coordinates.

    Parameters
    ----------
    E : 3-element numpy array
        The coordinates of the eye/camera.
    R : 3-element numpy array
        The coordinates of the center of the view box.
    V : 3-element numpy array
        Unit vector in the direction of the vertical axis.
    roll : float
        The roll angle in radians.

    Returns
    -------
    u : 3-element numpy array
        Unit vector pointing towards the right of the screen.
    v : 3-element numpy array
        Unit vector pointing towards the top of the screen.
    w : 3-element numpy array
        Unit vector pointing out of the screen.
    """
    w = (E - R)
    w = w/np.linalg.norm(w)
    u = np.cross(V, w)
    u = u/np.linalg.norm(u)
    v = np.cross(w, u)  # Will be a unit vector

    # Save some computation for the default roll=0
    if roll != 0:
        # A positive rotation of the camera is a negative rotation of the world
        Rroll = _rotation_about_vector(w, -roll)
        u = np.dot(Rroll, u)
        v = np.dot(Rroll, v)
    return u, v, w

