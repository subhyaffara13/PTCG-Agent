
def test_empty_arrays():
    # Check that plotting an empty array with a dtype works
    plt.scatter(np.array([], dtype='datetime64[ns]'), np.array([]))

