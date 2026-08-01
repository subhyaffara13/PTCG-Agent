
def get_viewport():
    """
    Returns the current viewport.
    """
    m = (c_int*4)()
    pgl.glGetIntegerv(pgl.GL_VIEWPORT, m)
    return m

