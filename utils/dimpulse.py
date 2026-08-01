
def dimpulse(system, x0=None, t=None, n=None):
    r"""Impulse response of discrete-time system.

    Parameters
    ----------
        system : dlti | tuple
        An instance of the LTI class `dlti` or a tuple describing the system.
        The number of elements in the tuple determine the interpretation. I.e.:

        * ``system``: Instance of LTI class `dlti`. Note that derived instances, such
          as instances of `TransferFunction`, `ZerosPolesGain`, or `StateSpace`, are
          allowed as well.
        * ``(num, den, dt)``: Rational polynomial as described in `TransferFunction`.
          The coefficients of the polynomials should be specified in descending
          exponent order,  e.g., z² + 3z + 5 would be represented as ``[1, 3, 5]``.
        * ``(zeros, poles, gain, dt)``:  Zeros, poles, gain form as described
          in `ZerosPolesGain`.
        * ``(A, B, C, D, dt)``: State-space form as described in `StateSpace`.

    x0 : array_like, optional
        Initial state-vector.  Defaults to zero.
    t : array_like, optional
        Time points.  Computed if not given.
    n : int, optional
        The number of time points to compute (if `t` is not given).

    Returns
    -------
    tout : ndarray
        Time values for the output, as a 1-D array.
    yout : tuple of ndarray
        Impulse response of system.  Each element of the tuple represents
        the output of the system based on an impulse in each input.

    See Also
    --------
    impulse, dstep, dlsim, cont2discrete

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    ...
    >>> dt = 1  # sampling interval is one => time unit is sample number
    >>> bb, aa = signal.butter(3, 0.25, fs=1/dt)
    >>> t, y = signal.dimpulse((bb, aa, dt), n=25)
    ...
    >>> fig0, ax0 = plt.subplots()
    >>> ax0.step(t, np.squeeze(y), '.-', where='post')
    >>> ax0.set_title(r"Impulse Response of a $3^\text{rd}$ Order Butterworth Filter")
    >>> ax0.set(xlabel='Sample number', ylabel='Amplitude')
    >>> ax0.grid()
    >>> plt.show()
    """
    # Convert system to dlti-StateSpace
    if isinstance(system, dlti):
        system = system._as_ss()
    elif isinstance(system, lti):
        raise AttributeError('dimpulse can only be used with discrete-time '
                             'dlti systems.')
    else:
        system = dlti(*system[:-1], dt=system[-1])._as_ss()

    # Default to 100 samples if unspecified
    if n is None:
        n = 100

    # If time is not specified, use the number of samples
    # and system dt
    if t is None:
        t = np.linspace(0, n * system.dt, n, endpoint=False)
    else:
        t = np.asarray(t)

    # For each input, implement a step change
    yout = None
    for i in range(0, system.inputs):
        u = np.zeros((t.shape[0], system.inputs))
        u[0, i] = 1.0

        one_output = dlsim(system, u, t=t, x0=x0)

        if yout is None:
            yout = (one_output[1],)
        else:
            yout = yout + (one_output[1],)

        tout = one_output[0]

    return tout, yout

