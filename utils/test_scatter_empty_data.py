
def test_scatter_empty_data():
    # making sure this does not raise an exception
    plt.scatter([], [])
    plt.scatter([], [], s=[], c=[])

