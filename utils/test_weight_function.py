
def test_weight_function():
    G = nx.cycle_graph(4)

    def my_weight(u, v, d):
        if u == 2 and v == 3:
            return None
        return u + v

    split = kernighan_lin_bisection(G, weight=my_weight)
    assert_partition_equal(split, ({1, 2}, {0, 3}))

