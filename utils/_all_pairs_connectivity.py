
def _all_pairs_connectivity(G, cc, k, memo):
    # Brute force check
    for u, v in it.combinations(cc, 2):
        # Use a memoization dict to save on computation
        connectivity = _memo_connectivity(G, u, v, memo)
        if G.is_directed():
            connectivity = min(connectivity, _memo_connectivity(G, v, u, memo))
        assert connectivity >= k

