
def solve_discrete_are(a, b, q, r, e=None, s=None, balanced=True):
    r"""
    Solves the discrete-time algebraic Riccati equation (DARE).

    The DARE is defined as

    .. math::

          A^HXA - X - (A^HXB) (R + B^HXB)^{-1} (B^HXA) + Q = 0

    The limitations for a solution to exist are :

    * All eigenvalues of :math:`A` outside the unit disc, should be
      controllable.

    * The associated symplectic pencil (See Notes), should have
      eigenvalues sufficiently away from the unit circle.

    Moreover, if ``e`` and ``s`` are not both precisely ``None``, then the
    generalized version of DARE

    .. math::

          A^HXA - E^HXE - (A^HXB+S) (R+B^HXB)^{-1} (B^HXA+S^H) + Q = 0

    is solved. When omitted, ``e`` is assumed to be the identity and ``s``
    is assumed to be the zero matrix.

    The documentation is written assuming array arguments are of specified
    "core" shapes. However, array argument(s) of this function may have additional
    "batch" dimensions prepended to the core shape. In this case, the array is treated
    as a batch of lower-dimensional slices; see :ref:`linalg_batch` for details.

    Parameters
    ----------
    a : (M, M) array_like
        Square matrix
    b : (M, N) array_like
        Input
    q : (M, M) array_like
        Input
    r : (N, N) array_like
        Square matrix
    e : (M, M) array_like, optional
        Nonsingular square matrix
    s : (M, N) array_like, optional
        Input
    balanced : bool
        The boolean that indicates whether a balancing step is performed
        on the data. The default is set to True.

    Returns
    -------
    x : (M, M) ndarray
        Solution to the discrete algebraic Riccati equation.

    Raises
    ------
    LinAlgError
        For cases where the stable subspace of the pencil could not be
        isolated. See Notes section and the references for details.

    See Also
    --------
    solve_continuous_are : Solves the continuous algebraic Riccati equation

    Notes
    -----
    The equation is solved by forming the extended symplectic matrix pencil,
    as described in [1]_, :math:`H - \lambda J` given by the block matrices ::

           [  A   0   B ]             [ E   0   B ]
           [ -Q  E^H -S ] - \lambda * [ 0  A^H  0 ]
           [ S^H  0   R ]             [ 0 -B^H  0 ]

    and using a QZ decomposition method.

    In this algorithm, the fail conditions are linked to the symmetry
    of the product :math:`U_2 U_1^{-1}` and condition number of
    :math:`U_1`. Here, :math:`U` is the 2m-by-m matrix that holds the
    eigenvectors spanning the stable subspace with 2-m rows and partitioned
    into two m-row matrices. See [1]_ and [2]_ for more details.

    In order to improve the QZ decomposition accuracy, the pencil goes
    through a balancing step where the sum of absolute values of
    :math:`H` and :math:`J` rows/cols (after removing the diagonal entries)
    is balanced following the recipe given in [3]_. If the data has small
    numerical noise, balancing may amplify their effects and some clean up
    is required.

    .. versionadded:: 0.11.0

    References
    ----------
    .. [1]  P. van Dooren , "A Generalized Eigenvalue Approach For Solving
       Riccati Equations.", SIAM Journal on Scientific and Statistical
       Computing, Vol.2(2), :doi:`10.1137/0902010`

    .. [2] A.J. Laub, "A Schur Method for Solving Algebraic Riccati
       Equations.", Massachusetts Institute of Technology. Laboratory for
       Information and Decision Systems. LIDS-R ; 859. Available online :
       http://hdl.handle.net/1721.1/1301

    .. [3] P. Benner, "Symplectic Balancing of Hamiltonian Matrices", 2001,
       SIAM J. Sci. Comput., 2001, Vol.22(5), :doi:`10.1137/S1064827500367993`

    Examples
    --------
    Given `a`, `b`, `q`, and `r` solve for `x`:

    >>> import numpy as np
    >>> from scipy import linalg as la
    >>> a = np.array([[0, 1], [0, -1]])
    >>> b = np.array([[1, 0], [2, 1]])
    >>> q = np.array([[-4, -4], [-4, 7]])
    >>> r = np.array([[9, 3], [3, 1]])
    >>> x = la.solve_discrete_are(a, b, q, r)
    >>> x
    array([[-4., -4.],
           [-4.,  7.]])
    >>> R = la.solve(r + b.T.dot(x).dot(b), b.T.dot(x).dot(a))
    >>> np.allclose(a.T.dot(x).dot(a) - x - a.T.dot(x).dot(b).dot(R), -q)
    True

    """
    # ensure that all arguments are present when using `_apply_over_batch` (gh-23336)
    return _solve_discrete_are(a, b, q, r, e, s, balanced)

