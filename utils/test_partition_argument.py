
def test_partition_argument():
    G = nx.barbell_graph(3, 0)
    partition = [{0, 1, 2}, {3, 4, 5}]
    split = kernighan_lin_bisection(G, partition)
    assert_partition_equal(split, partition)

