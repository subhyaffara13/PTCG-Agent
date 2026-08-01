
def test_network_simplex_faux_infinity(
    faux_inf_example, large_capacity, large_demand, large_weight
):
    """network_simplex should not raise an exception as a result of faux_infinity
    for these cases. See gh-7562"""
    G = faux_inf_example
    lv = 1_000_000_000

    # Modify the base graph with combinations of large values for capacity,
    # demand, and weight to probe faux_inifity
    if large_capacity:
        G["s0"]["ns"]["capacity"] = lv
    if large_demand:
        G.nodes["s0"]["demand"] = -lv
        G.nodes["c1"]["demand"] = lv
    if large_weight:
        G["s1"]["ns"]["weight"] = lv

    # Execute without raising
    fc, fd = nx.network_simplex(G)

