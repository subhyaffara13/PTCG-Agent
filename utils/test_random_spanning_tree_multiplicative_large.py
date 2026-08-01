
def test_random_spanning_tree_multiplicative_large():
    """
    Sample many trees from the distribution created in the last test
    """
    from math import exp
    from random import Random

    pytest.importorskip("numpy")
    stats = pytest.importorskip("scipy.stats")

    gamma = {
        (0, 1): -0.6383,
        (0, 2): -0.6827,
        (0, 5): 0,
        (1, 2): -1.0781,
        (1, 4): 0,
        (2, 3): 0,
        (5, 3): -0.2820,
        (5, 4): -0.3327,
        (4, 3): -0.9927,
    }

    # The undirected support of gamma
    G = nx.Graph()
    for u, v in gamma:
        G.add_edge(u, v, lambda_key=exp(gamma[(u, v)]))

    # Find the multiplicative weight for each tree.
    total_weight = 0
    tree_expected = {}
    for t in nx.SpanningTreeIterator(G):
        # Find the multiplicative weight of the spanning tree
        weight = 1
        for u, v, d in t.edges(data="lambda_key"):
            weight *= d
        tree_expected[t] = weight
        total_weight += weight

    # Assert that every tree has an entry in the expected distribution
    assert len(tree_expected) == 75

    # Set the sample size and then calculate the expected number of times we
    # expect to see each tree. This test uses a near minimum sample size where
    # the most unlikely tree has an expected frequency of 5.15.
    # (Minimum required is 5)
    #
    # Here we also initialize the tree_actual dict so that we know the keys
    # match between the two. We will later take advantage of the fact that since
    # python 3.7 dict order is guaranteed so the expected and actual data will
    # have the same order.
    sample_size = 1200
    tree_actual = {}
    for t in tree_expected:
        tree_expected[t] = (tree_expected[t] / total_weight) * sample_size
        tree_actual[t] = 0

    # Sample the spanning trees
    #
    # Assert that they are actually trees and record which of the 75 trees we
    # have sampled.
    #
    # For repeatability, we want to take advantage of the decorators in NetworkX
    # to randomly sample the same sample each time. However, if we pass in a
    # constant seed to sample_spanning_tree we will get the same tree each time.
    # Instead, we can create our own random number generator with a fixed seed
    # and pass those into sample_spanning_tree.
    rng = Random(37)
    for _ in range(sample_size):
        sampled_tree = nx.random_spanning_tree(G, "lambda_key", seed=rng)
        assert nx.is_tree(sampled_tree)

        for t in tree_expected:
            if nx.utils.edges_equal(t.edges, sampled_tree.edges):
                tree_actual[t] += 1
                break

    # Conduct a Chi squared test to see if the actual distribution matches the
    # expected one at an alpha = 0.05 significance level.
    #
    # H_0: The distribution of trees in tree_actual matches the normalized product
    # of the edge weights in the tree.
    #
    # H_a: The distribution of trees in tree_actual follows some other
    # distribution of spanning trees.
    _, p = stats.chisquare(list(tree_actual.values()), list(tree_expected.values()))

    # Assert that p is greater than the significance level so that we do not
    # reject the null hypothesis
    assert not p < 0.05

