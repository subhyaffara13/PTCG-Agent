
def test_Joint():
    parent = RigidBody('parent')
    child = RigidBody('child')
    raises(TypeError, lambda: Joint('J', parent, child))

