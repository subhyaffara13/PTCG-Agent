
def cont2discrete(system, dt, method="zoh", alpha=None):
    """
    Transform a continuous to a discrete state-space system.

    Parameters
    ----------
    system : a tuple describing the system or an instance of `lti`
        The following gives the number of elements in the tuple and
        the interpretation:

        * 1: (instance of `lti`)
        * 2: (num, den)
        * 3: (zeros, poles, gain)
        * 4: (A, B, C, D)

    dt : float
        The discretization time step.
    method : str, optional
        Which method to use:

        * gbt: generalized bilinear transformation
        * bilinear: Tustin's approximation ("gbt" with alpha=0.5)
        * euler: Euler (or forward differencing) method ("gbt" with alpha=0)
        * backward_diff: Backwards differencing ("gbt" with alpha=1.0)
        * zoh: zero-order hold (default)
        * foh: first-order hold (*versionadded: 1.3.0*)
        * impulse: equivalent impulse response (*versionadded: 1.3.0*)

    alpha : float within [0, 1], optional
        The generalized bilinear transformation weighting parameter, which
        should only be specified with method="gbt", and is ignored otherwise

    Returns
    -------
    sysd : tuple containing the discrete system
        Based on the input type, the output will be of the form

        * (num, den, dt)   for transfer function input
        * (zeros, poles, gain, dt)   for zeros-poles-gain input
        * (A, B, C, D, dt) for state-space system input

    Notes
    -----
    By default, the routine uses a Zero-Order Hold (zoh) method to perform
    the transformation. Alternatively, a generalized bilinear transformation
    may be used, which includes the common Tustin's bilinear approximation,
    an Euler's method technique, or a backwards differencing technique.

    The Zero-Order Hold (zoh) method is based on [1]_, the generalized bilinear
    approximation is based on [2]_ and [3]_, the First-Order Hold (foh) method
    is based on [4]_.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Discretization#Discretization_of_linear_state_space_models

    .. [2] http://techteach.no/publications/discretetime_signals_systems/discrete.pdf

    .. [3] G. Zhang, X. Chen, and T. Chen, Digital redesign via the generalized
        bilinear transformation, Int. J. Control, vol. 82, no. 4, pp. 741-754,
        2009.
        (https://www.mypolyuweb.hk/~magzhang/Research/ZCC09_IJC.pdf)

    .. [4] G. F. Franklin, J. D. Powell, and M. L. Workman, Digital control
        of dynamic systems, 3rd ed. Menlo Park, Calif: Addison-Wesley,
        pp. 204-206, 1998.

    Examples
    --------
    We can transform a continuous state-space system to a discrete one:

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.signal import cont2discrete, lti, dlti, dstep

    Define a continuous state-space system.

    >>> A = np.array([[0, 1],[-10., -3]])
    >>> B = np.array([[0],[10.]])
    >>> C = np.array([[1., 0]])
    >>> D = np.array([[0.]])
    >>> l_system = lti(A, B, C, D)
    >>> t, x = l_system.step(T=np.linspace(0, 5, 100))
    >>> fig, ax = plt.subplots()
    >>> ax.plot(t, x, label='Continuous', linewidth=3)

    Transform it to a discrete state-space system using several methods.

    >>> dt = 0.1
    >>> for method in ['zoh', 'bilinear', 'euler', 'backward_diff', 'foh', 'impulse']:
    ...    d_system = cont2discrete((A, B, C, D), dt, method=method)
    ...    s, x_d = dstep(d_system)
    ...    ax.step(s, np.squeeze(x_d), label=method, where='post')
    >>> ax.axis([t[0], t[-1], x[0], 1.4])
    >>> ax.legend(loc='best')
    >>> fig.tight_layout()
    >>> plt.show()

    """
    if hasattr(system, 'to_discrete') and callable(system.to_discrete):
        return system.to_discrete(dt=dt, method=method, alpha=alpha)

    if len(system) == 2:
        sysd = cont2discrete(tf2ss(system[0], system[1]), dt, method=method,
                             alpha=alpha)
        return ss2tf(sysd[0], sysd[1], sysd[2], sysd[3]) + (dt,)
    elif len(system) == 3:
        sysd = cont2discrete(zpk2ss(system[0], system[1], system[2]), dt,
                             method=method, alpha=alpha)
        return ss2zpk(sysd[0], sysd[1], sysd[2], sysd[3]) + (dt,)
    elif len(system) == 4:
        a, b, c, d = system
    else:
        raise ValueError("First argument must either be a tuple of 2 (tf), "
                         "3 (zpk), or 4 (ss) arrays.")

    if method == 'gbt':
        if alpha is None:
            raise ValueError("Alpha parameter must be specified for the "
                             "generalized bilinear transform (gbt) method")
        elif alpha < 0 or alpha > 1:
            raise ValueError("Alpha parameter must be within the interval "
                             "[0,1] for the gbt method")

    if method == 'gbt':
        # This parameter is used repeatedly - compute once here
        ima = np.eye(a.shape[0]) - alpha*dt*a
        ad = linalg.solve(ima, np.eye(a.shape[0]) + (1.0-alpha)*dt*a)
        bd = linalg.solve(ima, dt*b)

        # Similarly solve for the output equation matrices
        cd = linalg.solve(ima.transpose(), c.transpose())
        cd = cd.transpose()
        dd = d + alpha*np.dot(c, bd)

    elif method == 'bilinear' or method == 'tustin':
        return cont2discrete(system, dt, method="gbt", alpha=0.5)

    elif method == 'euler' or method == 'forward_diff':
        return cont2discrete(system, dt, method="gbt", alpha=0.0)

    elif method == 'backward_diff':
        return cont2discrete(system, dt, method="gbt", alpha=1.0)

    elif method == 'zoh':
        # Build an exponential matrix
        em_upper = np.hstack((a, b))

        # Need to stack zeros under the a and b matrices
        em_lower = np.hstack((np.zeros((b.shape[1], a.shape[0])),
                              np.zeros((b.shape[1], b.shape[1]))))

        em = np.vstack((em_upper, em_lower))
        ms = linalg.expm(dt * em)

        # Dispose of the lower rows
        ms = ms[:a.shape[0], :]

        ad = ms[:, 0:a.shape[1]]
        bd = ms[:, a.shape[1]:]

        cd = c
        dd = d

    elif method == 'foh':
        # Size parameters for convenience
        n = a.shape[0]
        m = b.shape[1]

        # Build an exponential matrix similar to 'zoh' method
        em_upper = linalg.block_diag(np.block([a, b]) * dt, np.eye(m))
        em_lower = zeros((m, n + 2 * m))
        em = np.block([[em_upper], [em_lower]])

        ms = linalg.expm(em)

        # Get the three blocks from upper rows
        ms11 = ms[:n, 0:n]
        ms12 = ms[:n, n:n + m]
        ms13 = ms[:n, n + m:]

        ad = ms11
        bd = ms12 - ms13 + ms11 @ ms13
        cd = c
        dd = d + c @ ms13

    elif method == 'impulse':
        if not np.allclose(d, 0):
            raise ValueError("Impulse method is only applicable "
                             "to strictly proper systems")

        ad = linalg.expm(a * dt)
        bd = ad @ b * dt
        cd = c
        dd = c @ b * dt

    else:
        raise ValueError(f"Unknown transformation method '{method}'")

    return ad, bd, cd, dd, dt

