
def test_subspace_angles():
    H = hadamard(8, float)
    A = H[:, :3]
    B = H[:, 3:]
    assert_allclose(subspace_angles(A, B), [np.pi / 2.] * 3, atol=1e-14)
    assert_allclose(subspace_angles(B, A), [np.pi / 2.] * 3, atol=1e-14)
    for x in (A, B):
        assert_allclose(subspace_angles(x, x), np.zeros(x.shape[1]),
                        atol=1e-14)
    # From MATLAB function "subspace", which effectively only returns the
    # last value that we calculate
    x = np.array(
        [[0.537667139546100, 0.318765239858981, 3.578396939725760, 0.725404224946106],  # noqa: E501
         [1.833885014595086, -1.307688296305273, 2.769437029884877, -0.063054873189656],  # noqa: E501
         [-2.258846861003648, -0.433592022305684, -1.349886940156521, 0.714742903826096],  # noqa: E501
         [0.862173320368121, 0.342624466538650, 3.034923466331855, -0.204966058299775]])  # noqa: E501
    expected = 1.481454682101605
    assert_allclose(subspace_angles(x[:, :2], x[:, 2:])[0], expected,
                    rtol=1e-12)
    assert_allclose(subspace_angles(x[:, 2:], x[:, :2])[0], expected,
                    rtol=1e-12)
    expected = 0.746361174247302
    assert_allclose(subspace_angles(x[:, :2], x[:, [2]]), expected, rtol=1e-12)
    assert_allclose(subspace_angles(x[:, [2]], x[:, :2]), expected, rtol=1e-12)
    expected = 0.487163718534313
    assert_allclose(subspace_angles(x[:, :3], x[:, [3]]), expected, rtol=1e-12)
    assert_allclose(subspace_angles(x[:, [3]], x[:, :3]), expected, rtol=1e-12)
    expected = 0.328950515907756
    assert_allclose(subspace_angles(x[:, :2], x[:, 1:]), [expected, 0],
                    atol=1e-12)
    # Degenerate conditions
    assert_raises(ValueError, subspace_angles, x[0], x)
    assert_raises(ValueError, subspace_angles, x, x[0])
    assert_raises(ValueError, subspace_angles, x[:-1], x)

    # Test branch if mask.any is True:
    A = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1],
                  [0, 0, 0],
                  [0, 0, 0]])
    B = np.array([[1, 0, 0],
                  [0, 1, 0],
                  [0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 1]])
    expected = np.array([np.pi/2, 0, 0])
    assert_allclose(subspace_angles(A, B), expected, rtol=1e-12)

    # Complex
    # second column in "b" does not affect result, just there so that
    # b can have more cols than a, and vice-versa (both conditional code paths)
    a = [[1 + 1j], [0]]
    b = [[1 - 1j, 0], [0, 1]]
    assert_allclose(subspace_angles(a, b), 0., atol=1e-14)
    assert_allclose(subspace_angles(b, a), 0., atol=1e-14)

    # Empty
    a = np.empty((0, 0))
    b = np.empty((0, 0))
    assert_allclose(subspace_angles(a, b), np.empty((0,)))
    a = np.empty((2, 0))
    b = np.empty((2, 0))
    assert_allclose(subspace_angles(a, b), np.empty((0,)))
    a = np.empty((0, 2))
    b = np.empty((0, 3))
    assert_allclose(subspace_angles(a, b), np.empty((0,)))

