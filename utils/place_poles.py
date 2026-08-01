
def place_poles(A, B, poles, method="YT", rtol=1e-3, maxiter=30):
    """
    Compute K such that eigenvalues (A - dot(B, K))=poles.

    K is the gain matrix such as the plant described by the linear system
    ``AX+BU`` will have its closed-loop poles, i.e the eigenvalues ``A - B*K``,
    as close as possible to those asked for in poles.

    SISO, MISO and MIMO systems are supported.

    Parameters
    ----------
    A, B : ndarray
        State-space representation of linear system ``AX + BU``.
    poles : array_like
        Desired real poles and/or complex conjugates poles.
        Complex poles are only supported with ``method="YT"`` (default).
    method : {'YT', 'KNV0'}, optional
        Which method to choose to find the gain matrix K. One of:

        - 'YT': Yang Tits
        - 'KNV0': Kautsky, Nichols, Van Dooren update method 0

        See References and Notes for details on the algorithms.
    rtol : float, optional
        After each iteration the determinant of the eigenvectors of
        ``A - B*K`` is compared to its previous value, when the relative
        error between these two values becomes lower than `rtol` the algorithm
        stops.  Default is 1e-3.
    maxiter : int, optional
        Maximum number of iterations to compute the gain matrix.
        Default is 30.

    Returns
    -------
    full_state_feedback : Bunch object
        full_state_feedback is composed of:
            gain_matrix : 2-D ndarray
                The closed loop matrix K such as the eigenvalues of ``A-BK``
                are as close as possible to the requested poles.
            computed_poles : 1-D ndarray
                The poles corresponding to ``A-BK`` sorted as first the real
                poles in increasing order, then the complex conjugates in
                lexicographic order.
            requested_poles : 1-D ndarray
                The poles the algorithm was asked to place sorted as above,
                they may differ from what was achieved.
            X : 2-D ndarray
                The transfer matrix such as ``X * diag(poles) = (A - B*K)*X``
                (see Notes)
            rtol : float
                The relative tolerance achieved on ``det(X)`` (see Notes).
                `rtol` will be NaN if it is possible to solve the system
                ``diag(poles) = (A - B*K)``, or 0 when the optimization
                algorithms can't do anything i.e when ``B.shape[1] == 1``.
            nb_iter : int
                The number of iterations performed before converging.
                `nb_iter` will be NaN if it is possible to solve the system
                ``diag(poles) = (A - B*K)``, or 0 when the optimization
                algorithms can't do anything i.e when ``B.shape[1] == 1``.

    Notes
    -----
    The Tits and Yang (YT), [2]_ paper is an update of the original Kautsky et
    al. (KNV) paper [1]_.  KNV relies on rank-1 updates to find the transfer
    matrix X such that ``X * diag(poles) = (A - B*K)*X``, whereas YT uses
    rank-2 updates. This yields on average more robust solutions (see [2]_
    pp 21-22), furthermore the YT algorithm supports complex poles whereas KNV
    does not in its original version.  Only update method 0 proposed by KNV has
    been implemented here, hence the name ``'KNV0'``.

    KNV extended to complex poles is used in Matlab's ``place`` function, YT is
    distributed under a non-free licence by Slicot under the name ``robpole``.
    It is unclear and undocumented how KNV0 has been extended to complex poles
    (Tits and Yang claim on page 14 of their paper that their method can not be
    used to extend KNV to complex poles), therefore only YT supports them in
    this implementation.

    As the solution to the problem of pole placement is not unique for MIMO
    systems, both methods start with a tentative transfer matrix which is
    altered in various way to increase its determinant.  Both methods have been
    proven to converge to a stable solution, however depending on the way the
    initial transfer matrix is chosen they will converge to different
    solutions and therefore there is absolutely no guarantee that using
    ``'KNV0'`` will yield results similar to Matlab's or any other
    implementation of these algorithms.

    Using the default method ``'YT'`` should be fine in most cases; ``'KNV0'``
    is only provided because it is needed by ``'YT'`` in some specific cases.
    Furthermore ``'YT'`` gives on average more robust results than ``'KNV0'``
    when ``abs(det(X))`` is used as a robustness indicator.

    [2]_ is available as a technical report on the following URL:
    https://hdl.handle.net/1903/5598

    References
    ----------
    .. [1] J. Kautsky, N.K. Nichols and P. van Dooren, "Robust pole assignment
           in linear state feedback", International Journal of Control, Vol. 41
           pp. 1129-1155, 1985.
    .. [2] A.L. Tits and Y. Yang, "Globally convergent algorithms for robust
           pole assignment by state feedback", IEEE Transactions on Automatic
           Control, Vol. 41, pp. 1432-1452, 1996.

    Examples
    --------
    A simple example demonstrating real pole placement using both KNV and YT
    algorithms.  This is example number 1 from section 4 of the reference KNV
    publication ([1]_):

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt

    >>> A = np.array([[ 1.380,  -0.2077,  6.715, -5.676  ],
    ...               [-0.5814, -4.290,   0,      0.6750 ],
    ...               [ 1.067,   4.273,  -6.654,  5.893  ],
    ...               [ 0.0480,  4.273,   1.343, -2.104  ]])
    >>> B = np.array([[ 0,      5.679 ],
    ...               [ 1.136,  1.136 ],
    ...               [ 0,      0,    ],
    ...               [-3.146,  0     ]])
    >>> P = np.array([-0.2, -0.5, -5.0566, -8.6659])

    Now compute K with KNV method 0, with the default YT method and with the YT
    method while forcing 100 iterations of the algorithm and print some results
    after each call.

    >>> fsf1 = signal.place_poles(A, B, P, method='KNV0')
    >>> fsf1.gain_matrix
    array([[ 0.20071427, -0.96665799,  0.24066128, -0.10279785],
           [ 0.50587268,  0.57779091,  0.51795763, -0.41991442]])

    >>> fsf2 = signal.place_poles(A, B, P)  # uses YT method
    >>> fsf2.computed_poles
    array([-8.6659, -5.0566, -0.5   , -0.2   ])

    >>> fsf3 = signal.place_poles(A, B, P, rtol=-1, maxiter=100)
    >>> fsf3.X
    array([[ 0.52072442+0.j, -0.08409372+0.j, -0.56847937+0.j,  0.74823657+0.j],
           [-0.04977751+0.j, -0.80872954+0.j,  0.13566234+0.j, -0.29322906+0.j],
           [-0.82266932+0.j, -0.19168026+0.j, -0.56348322+0.j, -0.43815060+0.j],
           [ 0.22267347+0.j,  0.54967577+0.j, -0.58387806+0.j, -0.40271926+0.j]])

    The absolute value of the determinant of X is a good indicator to check the
    robustness of the results, both ``'KNV0'`` and ``'YT'`` aim at maximizing
    it.  Below a comparison of the robustness of the results above:

    >>> abs(np.linalg.det(fsf1.X)) < abs(np.linalg.det(fsf2.X))
    True
    >>> abs(np.linalg.det(fsf2.X)) < abs(np.linalg.det(fsf3.X))
    True

    Now a simple example for complex poles:

    >>> A = np.array([[ 0,  7/3.,  0,   0   ],
    ...               [ 0,   0,    0,  7/9. ],
    ...               [ 0,   0,    0,   0   ],
    ...               [ 0,   0,    0,   0   ]])
    >>> B = np.array([[ 0,  0 ],
    ...               [ 0,  0 ],
    ...               [ 1,  0 ],
    ...               [ 0,  1 ]])
    >>> P = np.array([-3, -1, -2-1j, -2+1j]) / 3.
    >>> fsf = signal.place_poles(A, B, P, method='YT')

    We can plot the desired and computed poles in the complex plane:

    >>> t = np.linspace(0, 2*np.pi, 401)
    >>> plt.plot(np.cos(t), np.sin(t), 'k--')  # unit circle
    >>> plt.plot(fsf.requested_poles.real, fsf.requested_poles.imag,
    ...          'wo', label='Desired')
    >>> plt.plot(fsf.computed_poles.real, fsf.computed_poles.imag, 'bx',
    ...          label='Placed')
    >>> plt.grid()
    >>> plt.axis('image')
    >>> plt.axis([-1.1, 1.1, -1.1, 1.1])
    >>> plt.legend(bbox_to_anchor=(1.05, 1), loc=2, numpoints=1)

    """
    # Move away all the inputs checking, it only adds noise to the code
    update_loop, poles = _valid_inputs(A, B, poles, method, rtol, maxiter)

    # The current value of the relative tolerance we achieved
    cur_rtol = 0
    # The number of iterations needed before converging
    nb_iter = 0

    # Step A: QR decomposition of B page 1132 KN
    # to debug with numpy qr uncomment the line below
    # u, z = np.linalg.qr(B, mode="complete")
    u, z = s_qr(B, mode="full")
    rankB = np.linalg.matrix_rank(B)
    u0 = u[:, :rankB]
    u1 = u[:, rankB:]
    z = z[:rankB, :]

    # If we can use the identity matrix as X the solution is obvious
    if B.shape[0] == rankB:
        # if B is square and full rank there is only one solution
        # such as (A+BK)=inv(X)*diag(P)*X with X=eye(A.shape[0])
        # i.e K=inv(B)*(diag(P)-A)
        # if B has as many lines as its rank (but not square) there are many
        # solutions and we can choose one using least squares
        # => use lstsq in both cases.
        # In both cases the transfer matrix X will be eye(A.shape[0]) and I
        # can hardly think of a better one so there is nothing to optimize
        #
        # for complex poles we use the following trick
        #
        # |a -b| has for eigenvalues a+b and a-b
        # |b a|
        #
        # |a+bi 0| has the obvious eigenvalues a+bi and a-bi
        # |0 a-bi|
        #
        # e.g solving the first one in R gives the solution
        # for the second one in C
        diag_poles = np.zeros(A.shape)
        idx = 0
        while idx < poles.shape[0]:
            p = poles[idx]
            diag_poles[idx, idx] = np.real(p)
            if ~np.isreal(p):
                diag_poles[idx, idx+1] = -np.imag(p)
                diag_poles[idx+1, idx+1] = np.real(p)
                diag_poles[idx+1, idx] = np.imag(p)
                idx += 1  # skip next one
            idx += 1
        gain_matrix = np.linalg.lstsq(B, diag_poles-A, rcond=-1)[0]
        transfer_matrix = np.eye(A.shape[0])
        cur_rtol = np.nan
        nb_iter = np.nan
    else:
        # step A (p1144 KNV) and beginning of step F: decompose
        # dot(U1.T, A-P[i]*I).T and build our set of transfer_matrix vectors
        # in the same loop
        ker_pole = []

        # flag to skip the conjugate of a complex pole
        skip_conjugate = False
        # select orthonormal base ker_pole for each Pole and vectors for
        # transfer_matrix
        for j in range(B.shape[0]):
            if skip_conjugate:
                skip_conjugate = False
                continue
            pole_space_j = np.dot(u1.T, A-poles[j]*np.eye(B.shape[0])).T

            # after QR Q=Q0|Q1
            # only Q0 is used to reconstruct  the qr'ed (dot Q, R) matrix.
            # Q1 is orthogonal to Q0 and will be multiplied by the zeros in
            # R when using mode "complete". In default mode Q1 and the zeros
            # in R are not computed

            # To debug with numpy qr uncomment the line below
            # Q, _ = np.linalg.qr(pole_space_j, mode="complete")
            Q, _ = s_qr(pole_space_j, mode="full")

            ker_pole_j = Q[:, pole_space_j.shape[1]:]

            # We want to select one vector in ker_pole_j to build the transfer
            # matrix, however qr returns sometimes vectors with zeros on the
            # same line for each pole and this yields very long convergence
            # times.
            # Or some other times a set of vectors, one with zero imaginary
            # part and one (or several) with imaginary parts. After trying
            # many ways to select the best possible one (eg ditch vectors
            # with zero imaginary part for complex poles) I ended up summing
            # all vectors in ker_pole_j, this solves 100% of the problems and
            # is a valid choice for transfer_matrix.
            # This way for complex poles we are sure to have a non zero
            # imaginary part that way, and the problem of lines full of zeros
            # in transfer_matrix is solved too as when a vector from
            # ker_pole_j has a zero the other one(s) when
            # ker_pole_j.shape[1]>1) for sure won't have a zero there.

            transfer_matrix_j = np.sum(ker_pole_j, axis=1)[:, np.newaxis]
            transfer_matrix_j = (transfer_matrix_j /
                                 np.linalg.norm(transfer_matrix_j))
            if ~np.isreal(poles[j]):  # complex pole
                transfer_matrix_j = np.hstack([np.real(transfer_matrix_j),
                                               np.imag(transfer_matrix_j)])
                ker_pole.extend([ker_pole_j, ker_pole_j])

                # Skip next pole as it is the conjugate
                skip_conjugate = True
            else:  # real pole, nothing to do
                ker_pole.append(ker_pole_j)

            if j == 0:
                transfer_matrix = transfer_matrix_j
            else:
                transfer_matrix = np.hstack((transfer_matrix, transfer_matrix_j))

        if rankB > 1:  # otherwise there is nothing we can optimize
            stop, cur_rtol, nb_iter = update_loop(ker_pole, transfer_matrix,
                                                  poles, B, maxiter, rtol)
            if not stop and rtol > 0:
                # if rtol<=0 the user has probably done that on purpose,
                # don't annoy them
                err_msg = (
                    "Convergence was not reached after maxiter iterations.\n"
                    f"You asked for a tolerance of {rtol}, we got {cur_rtol}."
                    )
                warnings.warn(err_msg, stacklevel=2)

        # reconstruct transfer_matrix to match complex conjugate pairs,
        # ie transfer_matrix_j/transfer_matrix_j+1 are
        # Re(Complex_pole), Im(Complex_pole) now and will be Re-Im/Re+Im after
        transfer_matrix = transfer_matrix.astype(complex)
        idx = 0
        while idx < poles.shape[0]-1:
            if ~np.isreal(poles[idx]):
                rel = transfer_matrix[:, idx].copy()
                img = transfer_matrix[:, idx+1]
                # rel will be an array referencing a column of transfer_matrix
                # if we don't copy() it will changer after the next line and
                # and the line after will not yield the correct value
                transfer_matrix[:, idx] = rel-1j*img
                transfer_matrix[:, idx+1] = rel+1j*img
                idx += 1  # skip next one
            idx += 1

        try:
            m = np.linalg.solve(transfer_matrix.T, np.dot(np.diag(poles),
                                                          transfer_matrix.T)).T
            gain_matrix = np.linalg.solve(z, np.dot(u0.T, m-A))
        except np.linalg.LinAlgError as e:
            raise ValueError("The poles you've chosen can't be placed. "
                             "Check the controllability matrix and try "
                             "another set of poles") from e

    # Beware: Kautsky solves A+BK but the usual form is A-BK
    gain_matrix = -gain_matrix
    # K still contains complex with ~=0j imaginary parts, get rid of them
    gain_matrix = np.real(gain_matrix)

    full_state_feedback = Bunch()
    full_state_feedback.gain_matrix = gain_matrix
    full_state_feedback.computed_poles = _order_complex_poles(
        np.linalg.eig(A - np.dot(B, gain_matrix))[0]
        )
    full_state_feedback.requested_poles = poles
    full_state_feedback.X = transfer_matrix
    full_state_feedback.rtol = cur_rtol
    full_state_feedback.nb_iter = nb_iter

    return full_state_feedback

