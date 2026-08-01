
def _energy_fruchterman_reingold(
    A, nnodes, k, pos, fixed, iterations, threshold, dim, gravity
):
    # Entry point for NetworkX graph is fruchterman_reingold_layout()
    # energy-based version
    import numpy as np
    import scipy as sp

    if gravity <= 0:
        raise ValueError(f"the gravity must be positive.")

    # make sure we have a Compressed Sparse Row format
    try:
        A = A.tocsr()
    except AttributeError:
        A = sp.sparse.csr_array(A)

    # Take absolute values of edge weights and symmetrize it
    A = np.abs(A)
    A = (A + A.T) / 2

    n_components, labels = sp.sparse.csgraph.connected_components(A, directed=False)
    bincount = np.bincount(labels)
    batchsize = 500

    def _cost_FR(x):
        pos = x.reshape((nnodes, dim))
        grad = np.zeros((nnodes, dim))
        cost = 0.0
        for l in range(0, nnodes, batchsize):
            r = min(l + batchsize, nnodes)
            # difference between selected node positions and all others
            delta = pos[l:r, np.newaxis, :] - pos[np.newaxis, :, :]
            # distance between points with a minimum distance of 1e-5
            distance2 = np.sum(delta * delta, axis=2)
            distance2 = np.maximum(distance2, 1e-10)
            distance = np.sqrt(distance2)
            # temporary variable for calculation
            Ad = A[l:r] * distance
            # attractive forces and repulsive forces
            grad[l:r] = 2 * np.einsum("ij,ijk->ik", Ad / k - k**2 / distance2, delta)
            # integrated attractive forces
            cost += np.sum(Ad * distance2) / (3 * k)
            # integrated repulsive forces
            cost -= k**2 * np.sum(np.log(distance))
        # gravitational force from the centroids of connected components to (0.5, ..., 0.5)^T
        centers = np.zeros((n_components, dim))
        np.add.at(centers, labels, pos)
        delta0 = centers / bincount[:, np.newaxis] - 0.5
        grad += gravity * delta0[labels]
        cost += gravity * 0.5 * np.sum(bincount * np.linalg.norm(delta0, axis=1) ** 2)
        # fix positions of fixed nodes
        grad[fixed] = 0.0
        return cost, grad.ravel()

    # Optimization of the energy function by L-BFGS algorithm
    options = {"maxiter": iterations, "gtol": threshold}
    return sp.optimize.minimize(
        _cost_FR, pos.ravel(), method="L-BFGS-B", jac=True, options=options
    ).x.reshape((nnodes, dim))

