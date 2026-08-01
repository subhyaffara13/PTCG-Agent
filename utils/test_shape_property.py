
def test_shape_property(xp, dim: int):
    shape = (dim,) * (dim - 1)
    tf = RigidTransform.from_translation(xp.zeros(shape + (3,)))
    assert tf.shape == shape

