import time

def test_joint_degree_graph(ntimes=10):
    for _ in range(ntimes):
        seed = int(time.time())

        n, m, p = 20, 10, 1
        # generate random graph with model powerlaw_cluster and calculate
        # its joint degree
        g = powerlaw_cluster_graph(n, m, p, seed=seed)
        joint_degrees_g = degree_mixing_dict(g, normalized=False)

        # generate simple undirected graph with given joint degree
        # joint_degrees_g
        G = joint_degree_graph(joint_degrees_g)
        joint_degrees_G = degree_mixing_dict(G, normalized=False)

        # assert that the given joint degree is equal to the generated
        # graph's joint degree
        assert joint_degrees_g == joint_degrees_G

