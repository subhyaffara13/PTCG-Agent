
def test_iter_buffering_growinner():
    # Test that the inner loop grows when no buffering is needed
    a = np.arange(30)
    i = nditer(a, ['buffered', 'growinner', 'external_loop'],
                           buffersize=5)
    # Should end up with just one inner loop here
    assert_equal(i[0].size, a.size)

