
def init_gl_stuff_old():
    """
    Initialise open GL, prior to core context 3.2
    """
    GL.glEnable(GL.GL_DEPTH_TEST)  # use our zbuffer

    # setup the camera
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(45.0, 640 / 480.0, 0.1, 100.0)  # setup lens
    GL.glTranslatef(0.0, 0.0, -3.0)  # move back
    GL.glRotatef(25, 1, 0, 0)  # orbit higher

