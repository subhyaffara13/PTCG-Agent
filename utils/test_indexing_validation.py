
def test_indexing_validation(xp):
    tf = RigidTransform.from_matrix(xp.eye(4))

    # Test indexing on single transform
    with pytest.raises(TypeError, match="Single transform is not subscriptable"):
        tf[0]

    with pytest.raises(TypeError, match="Single transform is not subscriptable"):
        tf[0:1]

    # Test length on single transform
    with pytest.raises(TypeError, match="Single transform has no len"):
        len(tf)

