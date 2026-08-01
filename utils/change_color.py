
def change_color(u, X, Y, N, H, F, C, L):
    """Change the color of 'u' from X to Y and update N, H, F, C."""
    assert F[u] == X and X != Y

    # Change the class of 'u' from X to Y
    F[u] = Y

    for k in C:
        # 'u' witnesses an edge from k -> Y instead of from k -> X now.
        if N[u, k] == 0:
            H[(X, k)] -= 1
            H[(Y, k)] += 1

    for v in L[u]:
        # 'v' has lost a neighbor in X and gained one in Y
        N[(v, X)] -= 1
        N[(v, Y)] += 1

        if N[(v, X)] == 0:
            # 'v' witnesses F[v] -> X
            H[(F[v], X)] += 1

        if N[(v, Y)] == 1:
            # 'v' no longer witnesses F[v] -> Y
            H[(F[v], Y)] -= 1

    C[X].remove(u)
    C[Y].append(u)

