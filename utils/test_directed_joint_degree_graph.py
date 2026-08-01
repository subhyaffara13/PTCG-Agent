
def test_directed_joint_degree_graph(n=15, m=100, ntimes=1000):
    for _ in range(ntimes):
        # generate gnm random graph and calculate its joint degree.
        g = gnm_random_graph(n, m, None, directed=True)

        # in-degree sequence of g as a list of integers.
        in_degrees = list(dict(g.in_degree()).values())
        # out-degree sequence of g as a list of integers.
        out_degrees = list(dict(g.out_degree()).values())
        nkk = degree_mixing_dict(g)

        # generate simple directed graph with given degree sequence and joint
        # degree matrix.
        G = directed_joint_degree_graph(in_degrees, out_degrees, nkk)

        # assert degree sequence correctness.
        assert in_degrees == list(dict(G.in_degree()).values())
        assert out_degrees == list(dict(G.out_degree()).values())
        # assert joint degree matrix correctness.
        assert nkk == degree_mixing_dict(G)

