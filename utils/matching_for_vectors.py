
def matching_for_vectors(m0, m1):
    n = len(m0)

    costs = [[vdiff_hypot2(v0, v1) for v1 in m1] for v0 in m0]
    (
        matching,
        matching_cost,
    ) = min_cost_perfect_bipartite_matching(costs)
    identity_cost = sum(costs[i][i] for i in range(n))
    return matching, matching_cost, identity_cost

