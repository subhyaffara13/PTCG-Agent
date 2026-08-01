
def matching_cost(G, matching):
    return sum(G[i][j] for i, j in enumerate(matching))

