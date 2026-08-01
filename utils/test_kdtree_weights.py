
def test_kdtree_weights(kdtree_type):

    data = np.linspace(0, 1, 4).reshape(-1, 1)
    tree1 = kdtree_type(data, leafsize=1)
    weights = np.ones(len(data), dtype='f4')

    nw = tree1._build_weights(weights)
    assert_array_equal(nw, [4, 2, 1, 1, 2, 1, 1])

    assert_raises(ValueError, tree1._build_weights, weights[:-1])

    for i in range(10):
        # since weights are uniform, these shall agree:
        c1 = tree1.count_neighbors(tree1, np.linspace(0, 10, i))
        c2 = tree1.count_neighbors(tree1, np.linspace(0, 10, i),
                weights=(weights, weights))
        c3 = tree1.count_neighbors(tree1, np.linspace(0, 10, i),
                weights=(weights, None))
        c4 = tree1.count_neighbors(tree1, np.linspace(0, 10, i),
                weights=(None, weights))
        tree1.count_neighbors(tree1, np.linspace(0, 10, i),
                weights=weights)

        assert_array_equal(c1, c2)
        assert_array_equal(c1, c3)
        assert_array_equal(c1, c4)

    for i in range(len(data)):
        # this tests removal of one data point by setting weight to 0
        w1 = weights.copy()
        w1[i] = 0
        data2 = data[w1 != 0]
        tree2 = kdtree_type(data2)

        c1 = tree1.count_neighbors(tree1, np.linspace(0, 10, 100),
                weights=(w1, w1))
        # "c2 is correct"
        c2 = tree2.count_neighbors(tree2, np.linspace(0, 10, 100))

        assert_array_equal(c1, c2)

        #this asserts for two different trees, singular weights
        # crashes
        assert_raises(ValueError, tree1.count_neighbors,
            tree2, np.linspace(0, 10, 100), weights=w1)

