
def test_copyto():
    a = np.arange(6, dtype='i4').reshape(2, 3)

    # Simple copy
    np.copyto(a, [[3, 1, 5], [6, 2, 1]])
    assert_equal(a, [[3, 1, 5], [6, 2, 1]])

    # Overlapping copy should work
    np.copyto(a[:, :2], a[::-1, 1::-1])
    assert_equal(a, [[2, 6, 5], [1, 3, 1]])

    # Defaults to 'same_kind' casting
    assert_raises(TypeError, np.copyto, a, 1.5)

    # Force a copy with 'unsafe' casting, truncating 1.5 to 1
    np.copyto(a, 1.5, casting='unsafe')
    assert_equal(a, 1)

    # Copying with a mask
    np.copyto(a, 3, where=[True, False, True])
    assert_equal(a, [[3, 1, 3], [3, 1, 3]])

    # Casting rule still applies with a mask
    assert_raises(TypeError, np.copyto, a, 3.5, where=[True, False, True])

    # Lists of integer 0's and 1's is ok too
    np.copyto(a, 4.0, casting='unsafe', where=[[0, 1, 1], [1, 0, 0]])
    assert_equal(a, [[3, 4, 4], [4, 1, 3]])

    # Overlapping copy with mask should work
    np.copyto(a[:, :2], a[::-1, 1::-1], where=[[0, 1], [1, 1]])
    assert_equal(a, [[3, 4, 4], [4, 3, 3]])

    # 'dst' must be an array
    assert_raises(TypeError, np.copyto, [1, 2, 3], [2, 3, 4])

