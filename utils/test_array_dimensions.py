
def test_array_dimensions(pcfunc):
    # Make sure we can set the 1D, 2D, and 3D array shapes
    z = np.arange(12).reshape(3, 4)
    pc = getattr(plt, pcfunc)(z)
    # 1D
    pc.set_array(z.ravel())
    pc.update_scalarmappable()
    # 2D
    pc.set_array(z)
    pc.update_scalarmappable()
    # 3D RGB is OK as well
    z = np.arange(36, dtype=np.uint8).reshape(3, 4, 3)
    pc.set_array(z)
    pc.update_scalarmappable()

