
def _lloyd_iteration(
    sample: np.ndarray,
    decay: float,
    qhull_options: str
) -> np.ndarray:
    """Lloyd-Max algorithm iteration.

    Based on the implementation of Stéfan van der Walt:

    https://github.com/stefanv/lloyd

    which is:

        Copyright (c) 2021-04-21 Stéfan van der Walt
        https://github.com/stefanv/lloyd
        MIT License

    Parameters
    ----------
    sample : array_like (n, d)
        The sample to iterate on.
    decay : float
        Relaxation decay. A positive value would move the samples toward
        their centroid, and negative value would move them away.
        1 would move the samples to their centroid.
    qhull_options : str
        Additional options to pass to Qhull. See Qhull manual
        for details. (Default: "Qbb Qc Qz Qj Qx" for ndim > 4 and
        "Qbb Qc Qz Qj" otherwise.)

    Returns
    -------
    sample : array_like (n, d)
        The sample after an iteration of Lloyd's algorithm.

    """
    new_sample = np.empty_like(sample)

    voronoi = Voronoi(sample, qhull_options=qhull_options)

    for ii, idx in enumerate(voronoi.point_region):
        # the region is a series of indices into self.voronoi.vertices
        # remove samples at infinity, designated by index -1
        region = [i for i in voronoi.regions[idx] if i != -1]

        # get the vertices for this region
        verts = voronoi.vertices[region]

        # clipping would be wrong, we need to intersect
        # verts = np.clip(verts, 0, 1)

        # move samples towards centroids:
        # Centroid in n-D is the mean for uniformly distributed nodes
        # of a geometry.
        centroid = np.mean(verts, axis=0)
        new_sample[ii] = sample[ii] + (centroid - sample[ii]) * decay

    # only update sample to centroid within the region
    is_valid = np.all(np.logical_and(new_sample >= 0, new_sample <= 1), axis=1)
    sample[is_valid] = new_sample[is_valid]

    return sample

