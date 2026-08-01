
def test_collection_norm_autoscale():
    # norm should be autoscaled when array is set, not deferred to draw time
    lines = np.arange(24).reshape((4, 3, 2))
    coll = mcollections.LineCollection(lines, array=np.arange(4))
    assert coll.norm(2) == 2 / 3
    # setting a new array shouldn't update the already scaled limits
    coll.set_array(np.arange(4) + 5)
    assert coll.norm(2) == 2 / 3

