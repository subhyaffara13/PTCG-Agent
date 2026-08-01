
def test_partition_argument_non_integer_nodes():
    G = nx.Graph([("A", "B"), ("A", "C"), ("B", "C"), ("C", "D")])
    partition = ({"A", "B"}, {"C", "D"})
    split = kernighan_lin_bisection(G, partition)
    assert_partition_equal(split, partition)

