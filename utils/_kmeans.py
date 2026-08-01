
def _kmeans(obs, guess, thresh=1e-5, xp=None):
    """ "raw" version of k-means.

    Returns
    -------
    code_book
        The lowest distortion codebook found.
    avg_dist
        The average distance a observation is from a code in the book.
        Lower means the code_book matches the data better.

    See Also
    --------
    kmeans : wrapper around k-means

    Examples
    --------
    Note: not whitened in this example.

    >>> import numpy as np
    >>> from scipy.cluster.vq import _kmeans
    >>> features  = np.array([[ 1.9,2.3],
    ...                       [ 1.5,2.5],
    ...                       [ 0.8,0.6],
    ...                       [ 0.4,1.8],
    ...                       [ 1.0,1.0]])
    >>> book = np.array((features[0],features[2]))
    >>> _kmeans(features,book)
    (array([[ 1.7       ,  2.4       ],
           [ 0.73333333,  1.13333333]]), 0.40563916697728591)

    """
    xp = np if xp is None else xp
    code_book = guess
    diff = xp.inf
    prev_avg_dists = deque([diff], maxlen=2)

    np_obs = np.asarray(obs)
    while diff > thresh:
        # compute membership and distances between obs and code_book
        obs_code, distort = vq(obs, code_book, check_finite=False)
        prev_avg_dists.append(xp.mean(distort, axis=-1))
        # recalc code_book as centroids of associated obs
        obs_code = np.asarray(obs_code)
        code_book, has_members = _vq.update_cluster_means(np_obs, obs_code,
                                                          code_book.shape[0])
        code_book = code_book[has_members]
        code_book = xp.asarray(code_book)
        diff = xp.abs(prev_avg_dists[0] - prev_avg_dists[1])

    _, final_distortions = vq(obs, code_book, check_finite=False)
    final_distortions_avg = xp.mean(final_distortions, axis=-1)
    return code_book, final_distortions_avg

