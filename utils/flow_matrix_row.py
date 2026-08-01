
def flow_matrix_row(G, weight=None, dtype=float, solver="lu"):
    # Generate a row of the current-flow matrix
    import numpy as np

    solvername = {
        "full": FullInverseLaplacian,
        "lu": SuperLUInverseLaplacian,
        "cg": CGInverseLaplacian,
    }
    n = G.number_of_nodes()
    L = nx.laplacian_matrix(G, nodelist=range(n), weight=weight).asformat("csc")
    L = L.astype(dtype)
    C = solvername[solver](L, dtype=dtype)  # initialize solver
    w = C.w  # w is the Laplacian matrix width
    # row-by-row flow matrix
    for u, v in sorted(sorted((u, v)) for u, v in G.edges()):
        B = np.zeros(w, dtype=dtype)
        c = G[u][v].get(weight, 1.0)
        B[u % w] = c
        B[v % w] = -c
        # get only the rows needed in the inverse laplacian
        # and multiply to get the flow matrix row
        row = B @ C.get_rows(u, v)
        yield row, (u, v)

