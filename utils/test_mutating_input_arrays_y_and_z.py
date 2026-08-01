
def test_mutating_input_arrays_y_and_z(fig_test, fig_ref):
    """
    Test to see if the `z` axis does not get mutated
    after a call to `Axes3D.plot`

    test cases came from GH#8990
    """
    ax1 = fig_test.add_subplot(111, projection='3d')
    x = [1, 2, 3]
    y = [0.0, 0.0, 0.0]
    z = [0.0, 0.0, 0.0]
    ax1.plot(x, y, z, 'o-')

    # mutate y,z to get a nontrivial line
    y[:] = [1, 2, 3]
    z[:] = [1, 2, 3]

    # draw the same plot without mutating x and y
    ax2 = fig_ref.add_subplot(111, projection='3d')
    x = [1, 2, 3]
    y = [0.0, 0.0, 0.0]
    z = [0.0, 0.0, 0.0]
    ax2.plot(x, y, z, 'o-')

