
def test_massive_arr_overflow():
    # on 64-bit systems we should be able to
    # handle arrays that exceed the indexing
    # size of a 32-bit signed integer
    try:
        import psutil
    except ModuleNotFoundError:
        pytest.skip("psutil required to check available memory")
    if psutil.virtual_memory().available < 80*2**30:
        # Don't run the test if there is less than 80 gig of RAM available.
        pytest.skip('insufficient memory available to run this test')
    size = int(3e9)
    arr1 = np.zeros(shape=(size, 2))
    arr2 = np.zeros(shape=(3, 2))
    arr1[size - 1] = [5, 5]
    actual = directed_hausdorff(u=arr1, v=arr2)
    assert_allclose(actual[0], 7.0710678118654755)
    assert_allclose(actual[1], size - 1)

