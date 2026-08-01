
def cdist(x1, x2, p=2.0, compute_mode="use_mm_for_euclid_dist_if_necessary"):
    # type: (Tensor, Tensor, float, str) -> (Tensor)
    r"""Computes batched the p-norm distance between each pair of the two collections of row vectors.

    Args:
        x1 (Tensor): input tensor where the last two dimensions represent the points and the feature dimension respectively.
            The shape can be :math:`D_1 \times D_2 \times \cdots \times D_n \times P \times M`,
            where :math:`P` is the number of points and :math:`M` is the feature dimension.
        x2 (Tensor): input tensor where the last two dimensions also represent the points and the feature dimension respectively.
            The shape can be :math:`D_1' \times D_2' \times \cdots \times D_m' \times R \times M`,
            where :math:`R` is the number of points and :math:`M` is the feature dimension,
            which should match the feature dimension of `x1`.
        p: p value for the p-norm distance to calculate between each vector pair
            :math:`\in [0, \infty]`.
        compute_mode:
            'use_mm_for_euclid_dist_if_necessary' - will use matrix multiplication approach to calculate
            euclidean distance (p = 2) if P > 25 or R > 25
            'use_mm_for_euclid_dist' - will always use matrix multiplication approach to calculate
            euclidean distance (p = 2)
            'donot_use_mm_for_euclid_dist' - will never use matrix multiplication approach to calculate
            euclidean distance (p = 2)
            Default: use_mm_for_euclid_dist_if_necessary.

    If x1 has shape :math:`B \times P \times M` and x2 has shape :math:`B \times R \times M` then the
    output will have shape :math:`B \times P \times R`.

    This function is equivalent to `scipy.spatial.distance.cdist(input,'minkowski', p=p)`
    if :math:`p \in (0, \infty)`. When :math:`p = 0` it is equivalent to
    `scipy.spatial.distance.cdist(input, 'hamming') * M`. When :math:`p = \infty`, the closest
    scipy function is `scipy.spatial.distance.cdist(xn, lambda x, y: np.abs(x - y).max())`.

    Example:

        >>> a = torch.tensor([[0.9041, 0.0196], [-0.3108, -2.4423], [-0.4821, 1.059]])
        >>> a
        tensor([[ 0.9041,  0.0196],
                [-0.3108, -2.4423],
                [-0.4821,  1.0590]])
        >>> b = torch.tensor([[-2.1763, -0.4713], [-0.6986, 1.3702]])
        >>> b
        tensor([[-2.1763, -0.4713],
                [-0.6986,  1.3702]])
        >>> torch.cdist(a, b, p=2)
        tensor([[3.1193, 2.0959],
                [2.7138, 3.8322],
                [2.2830, 0.3791]])
    """
    if has_torch_function_variadic(x1, x2):
        return handle_torch_function(
            cdist, (x1, x2), x1, x2, p=p, compute_mode=compute_mode
        )
    if compute_mode == "use_mm_for_euclid_dist_if_necessary":
        return _VF.cdist(x1, x2, p, None)  # type: ignore[attr-defined]
    elif compute_mode == "use_mm_for_euclid_dist":
        return _VF.cdist(x1, x2, p, 1)  # type: ignore[attr-defined]
    elif compute_mode == "donot_use_mm_for_euclid_dist":
        return _VF.cdist(x1, x2, p, 2)  # type: ignore[attr-defined]
    else:
        raise ValueError(f"{compute_mode} is not a valid value for compute_mode")


def cdist(
    g: jit_utils.GraphContext,
    x1,
    x2,
    p=2.0,
    compute_mode="use_mm_for_euclid_dist_if_necessary",
):
    # X1.shape = (B * P * D), X2.shape = (B * R * D)
    # In order to respect numpy style broadcasting as demonstrated in
    # https://github.com/onnx/onnx/blob/main/docs/Broadcasting.md
    # we unsqueeze both input tensors
    row_size_x1 = symbolic_helper._get_tensor_dim_size(x1, -2)
    row_size_x2 = symbolic_helper._get_tensor_dim_size(x2, -2)
    p_float = symbolic_helper._parse_arg(p, "f")
    compute_mode = symbolic_helper._parse_arg(compute_mode, "i")
    if p_float == 2.0 and (
        compute_mode == 1
        or (
            compute_mode is None
            and (
                row_size_x1 is None
                or row_size_x2 is None
                or (row_size_x1 >= 25 and row_size_x2 >= 25)
            )
        )
    ):
        return _euclidean_dist(g, x1, x2)
    rank = symbolic_helper._get_tensor_rank(x1)
    if rank is None:
        raise AssertionError("rank must be non-None")
    broadcasted_x1 = symbolic_helper._unsqueeze_helper(g, x1, [rank - 1])
    broadcasted_x2 = symbolic_helper._unsqueeze_helper(g, x2, [rank - 2])
    return pairwise_distance(
        g, broadcasted_x1, broadcasted_x2, p, eps=1e-06, keepdim=False
    )


def cdist(XA, XB, metric='euclidean', *, out=None, **kwargs):
    """
    Compute distance between each pair of the two collections of inputs.

    See Notes for common calling conventions.

    Parameters
    ----------
    XA : array_like
        An :math:`m_A` by :math:`n` array of :math:`m_A`
        original observations in an :math:`n`-dimensional space.
        Inputs are converted to float type.
    XB : array_like
        An :math:`m_B` by :math:`n` array of :math:`m_B`
        original observations in an :math:`n`-dimensional space.
        Inputs are converted to float type.
    metric : str or callable, optional
        The distance metric to use. If a string, the distance function can be
        'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation',
        'cosine', 'dice', 'euclidean', 'hamming', 'jaccard', 'jensenshannon',
        'mahalanobis', 'matching', 'minkowski', 'rogerstanimoto', 'russellrao',
        'seuclidean', 'sokalsneath', 'sqeuclidean', 'yule'.
    out : ndarray, optional
        Output array in which to place the result. It must have the same
        shape as the expected output.
    **kwargs : dict, optional
        Extra arguments to `metric`: refer to each metric documentation for a
        list of all possible arguments.

        Some possible arguments:

        p : scalar
        The p-norm to apply for Minkowski, weighted and unweighted.
        Default: 2.

        w : array_like
        The weight vector for metrics that support weights (e.g., Minkowski).

        V : array_like
        The variance vector for standardized Euclidean.
        Default: var(vstack([XA, XB]), axis=0, ddof=1)

        VI : array_like
        The inverse of the covariance matrix for Mahalanobis.
        Default: inv(cov(vstack([XA, XB].T))).T

        out : ndarray
        The output array
        If not None, the distance matrix Y is stored in this array.

    Returns
    -------
    Y : ndarray
        A :math:`m_A` by :math:`m_B` distance matrix is returned.
        For each :math:`i` and :math:`j`, the metric
        ``dist(u=XA[i], v=XB[j])`` is computed and stored in the
        :math:`ij` th entry.

    Raises
    ------
    ValueError
        An exception is thrown if `XA` and `XB` do not have
        the same number of columns.

    Notes
    -----
    The following are common calling conventions:

    1. ``Y = cdist(XA, XB, 'euclidean')``

       Computes the distance between :math:`m` points using
       Euclidean distance (2-norm) as the distance metric between the
       points. The points are arranged as :math:`m`
       :math:`n`-dimensional row vectors in the matrix X.

    2. ``Y = cdist(XA, XB, 'minkowski', p=2.)``

       Computes the distances using the Minkowski distance
       :math:`\\|u-v\\|_p` (:math:`p`-norm) where :math:`p > 0` (note
       that this is only a quasi-metric if :math:`0 < p < 1`).

    3. ``Y = cdist(XA, XB, 'cityblock')``

       Computes the city block or Manhattan distance between the
       points.

    4. ``Y = cdist(XA, XB, 'seuclidean', V=None)``

       Computes the standardized Euclidean distance. The standardized
       Euclidean distance between two n-vectors ``u`` and ``v`` is

       .. math::

          \\sqrt{\\sum {(u_i-v_i)^2 / V[x_i]}}.

       V is the variance vector; V[i] is the variance computed over all
       the i'th components of the points. If not passed, it is
       automatically computed.

    5. ``Y = cdist(XA, XB, 'sqeuclidean')``

       Computes the squared Euclidean distance :math:`\\|u-v\\|_2^2` between
       the vectors.

    6. ``Y = cdist(XA, XB, 'cosine')``

       Computes the cosine distance between vectors u and v,

       .. math::

          1 - \\frac{u \\cdot v}
                   {{\\|u\\|}_2 {\\|v\\|}_2}

       where :math:`\\|*\\|_2` is the 2-norm of its argument ``*``, and
       :math:`u \\cdot v` is the dot product of :math:`u` and :math:`v`.

    7. ``Y = cdist(XA, XB, 'correlation')``

       Computes the correlation distance between vectors u and v. This is

       .. math::

          1 - \\frac{(u - \\bar{u}) \\cdot (v - \\bar{v})}
                   {{\\|(u - \\bar{u})\\|}_2 {\\|(v - \\bar{v})\\|}_2}

       where :math:`\\bar{v}` is the mean of the elements of vector v,
       and :math:`x \\cdot y` is the dot product of :math:`x` and :math:`y`.


    8. ``Y = cdist(XA, XB, 'hamming')``

       Computes the normalized Hamming distance, or the proportion of
       those vector elements between two n-vectors ``u`` and ``v``
       which disagree. To save memory, the matrix ``X`` can be of type
       boolean.

    9. ``Y = cdist(XA, XB, 'jaccard')``

       Computes the Jaccard distance between the points. Given two
       vectors, ``u`` and ``v``, the Jaccard distance is the
       proportion of those elements ``u[i]`` and ``v[i]`` that
       disagree where at least one of them is non-zero.

    10. ``Y = cdist(XA, XB, 'jensenshannon')``

        Computes the Jensen-Shannon distance between two probability arrays.
        Given two probability vectors, :math:`p` and :math:`q`, the
        Jensen-Shannon distance is

        .. math::

           \\sqrt{\\frac{D(p \\parallel m) + D(q \\parallel m)}{2}}

        where :math:`m` is the pointwise mean of :math:`p` and :math:`q`
        and :math:`D` is the Kullback-Leibler divergence.

    11. ``Y = cdist(XA, XB, 'chebyshev')``

        Computes the Chebyshev distance between the points. The
        Chebyshev distance between two n-vectors ``u`` and ``v`` is the
        maximum norm-1 distance between their respective elements. More
        precisely, the distance is given by

        .. math::

           d(u,v) = \\max_i {|u_i-v_i|}.

    12. ``Y = cdist(XA, XB, 'canberra')``

        Computes the Canberra distance between the points. The
        Canberra distance between two points ``u`` and ``v`` is

        .. math::

          d(u,v) = \\sum_i \\frac{|u_i-v_i|}
                               {|u_i|+|v_i|}.

    13. ``Y = cdist(XA, XB, 'braycurtis')``

        Computes the Bray-Curtis distance between the points. The
        Bray-Curtis distance between two points ``u`` and ``v`` is


        .. math::

             d(u,v) = \\frac{\\sum_i (|u_i-v_i|)}
                           {\\sum_i (|u_i+v_i|)}

    14. ``Y = cdist(XA, XB, 'mahalanobis', VI=None)``

        Computes the Mahalanobis distance between the points. The
        Mahalanobis distance between two points ``u`` and ``v`` is
        :math:`\\sqrt{(u-v)(1/V)(u-v)^T}` where :math:`(1/V)` (the ``VI``
        variable) is the inverse covariance. If ``VI`` is not None,
        ``VI`` will be used as the inverse covariance matrix.

    15. ``Y = cdist(XA, XB, 'yule')``

        Computes the Yule distance between the boolean
        vectors. (see `yule` function documentation)

    16. ``Y = cdist(XA, XB, 'matching')``

        Synonym for 'hamming'.

    17. ``Y = cdist(XA, XB, 'dice')``

        Computes the Dice distance between the boolean vectors. (see
        `dice` function documentation).

    18. ``Y = cdist(XA, XB, 'rogerstanimoto')``

        Computes the Rogers-Tanimoto distance between the boolean
        vectors. (see `rogerstanimoto` function documentation)

    19. ``Y = cdist(XA, XB, 'russellrao')``

        Computes the Russell-Rao distance between the boolean
        vectors. (see `russellrao` function documentation)

    20. ``Y = cdist(XA, XB, 'sokalsneath')``

        Computes the Sokal-Sneath distance between the vectors. (see
        `sokalsneath` function documentation)

    21. ``Y = cdist(XA, XB, f)``

        Computes the distance between all pairs of vectors in X
        using the user supplied 2-arity function f. For example,
        Euclidean distance between the vectors could be computed
        as follows::

          dm = cdist(XA, XB, lambda u, v: np.sqrt(((u-v)**2).sum()))

        Note that you should avoid passing a reference to one of
        the distance functions defined in this library. For example,::

          dm = cdist(XA, XB, sokalsneath)

        would calculate the pair-wise distances between the vectors in
        X using the Python function `sokalsneath`. This would result in
        sokalsneath being called :math:`{n \\choose 2}` times, which
        is inefficient. Instead, the optimized C version is more
        efficient, and we call it using the following syntax::

          dm = cdist(XA, XB, 'sokalsneath')

    Examples
    --------
    Find the Euclidean distances between four 2-D coordinates:

    >>> from scipy.spatial import distance
    >>> import numpy as np
    >>> coords = [(35.0456, -85.2672),
    ...           (35.1174, -89.9711),
    ...           (35.9728, -83.9422),
    ...           (36.1667, -86.7833)]
    >>> distance.cdist(coords, coords, 'euclidean')
    array([[ 0.    ,  4.7044,  1.6172,  1.8856],
           [ 4.7044,  0.    ,  6.0893,  3.3561],
           [ 1.6172,  6.0893,  0.    ,  2.8477],
           [ 1.8856,  3.3561,  2.8477,  0.    ]])


    Find the Manhattan distance from a 3-D point to the corners of the unit
    cube:

    >>> a = np.array([[0, 0, 0],
    ...               [0, 0, 1],
    ...               [0, 1, 0],
    ...               [0, 1, 1],
    ...               [1, 0, 0],
    ...               [1, 0, 1],
    ...               [1, 1, 0],
    ...               [1, 1, 1]])
    >>> b = np.array([[ 0.1,  0.2,  0.4]])
    >>> distance.cdist(a, b, 'cityblock')
    array([[ 0.7],
           [ 0.9],
           [ 1.3],
           [ 1.5],
           [ 1.5],
           [ 1.7],
           [ 2.1],
           [ 2.3]])

    """
    # You can also call this as:
    #     Y = cdist(XA, XB, 'test_abc')
    # where 'abc' is the metric being tested.  This computes the distance
    # between all pairs of vectors in XA and XB using the distance metric 'abc'
    # but with a more succinct, verifiable, but less efficient implementation.

    XA = np.asarray(XA)
    XB = np.asarray(XB)

    s = XA.shape
    sB = XB.shape

    if len(s) != 2:
        raise ValueError('XA must be a 2-dimensional array.')
    if len(sB) != 2:
        raise ValueError('XB must be a 2-dimensional array.')
    if s[1] != sB[1]:
        raise ValueError('XA and XB must have the same number of columns '
                         '(i.e. feature dimension.)')

    mA = s[0]
    mB = sB[0]
    n = s[1]

    if callable(metric):
        mstr = getattr(metric, '__name__', 'Unknown')
        metric_info = _METRIC_ALIAS.get(mstr, None)
        if metric_info is not None:
            XA, XB, typ, kwargs = _validate_cdist_input(
                XA, XB, mA, mB, n, metric_info, **kwargs)
        return _cdist_callable(XA, XB, metric=metric, out=out, **kwargs)
    elif isinstance(metric, str):
        mstr = metric.lower()
        metric_info = _METRIC_ALIAS.get(mstr, None)
        if metric_info is not None:
            cdist_fn = metric_info.cdist_func
            return cdist_fn(XA, XB, out=out, **kwargs)
        elif mstr.startswith("test_"):
            metric_info = _TEST_METRICS.get(mstr, None)
            if metric_info is None:
                raise ValueError(f'Unknown "Test" Distance Metric: {mstr[5:]}')
            XA, XB, typ, kwargs = _validate_cdist_input(
                XA, XB, mA, mB, n, metric_info, **kwargs)
            return _cdist_callable(
                XA, XB, metric=metric_info.dist_func, out=out, **kwargs)
        else:
            raise ValueError(f'Unknown Distance Metric: {mstr}')
    else:
        raise TypeError('2nd argument metric must be a string identifier '
                        'or a function.')

