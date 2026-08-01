
def test_quadmesh_set_array():
    x = np.arange(4)
    y = np.arange(4)
    z = np.arange(9).reshape((3, 3))
    fig, ax = plt.subplots()
    coll = ax.pcolormesh(x, y, np.ones(z.shape))
    # Test that the collection is able to update with a 2d array
    coll.set_array(z)
    fig.canvas.draw()
    assert np.array_equal(coll.get_array(), z)

    # Check that pre-flattened arrays work too
    coll.set_array(np.ones(9))
    fig.canvas.draw()
    assert np.array_equal(coll.get_array(), np.ones(9))

    z = np.arange(16).reshape((4, 4))
    fig, ax = plt.subplots()
    coll = ax.pcolormesh(x, y, np.ones(z.shape), shading='gouraud')
    # Test that the collection is able to update with a 2d array
    coll.set_array(z)
    fig.canvas.draw()
    assert np.array_equal(coll.get_array(), z)

    # Check that pre-flattened arrays work too
    coll.set_array(np.ones(16))
    fig.canvas.draw()
    assert np.array_equal(coll.get_array(), np.ones(16))

