
def step(
    x: ArrayLike,
    y: ArrayLike,
    *args,
    where: Literal["pre", "post", "mid"] = "pre",
    data: DataParamType = None,
    **kwargs,
) -> list[Line2D]:
    return gca().step(
        x,
        y,
        *args,
        where=where,
        **({"data": data} if data is not None else {}),
        **kwargs,
    )


def step(system, X0=None, T=None, N=None):
    """Step response of continuous-time system.

    Parameters
    ----------
    system : an instance of the LTI class or a tuple of array_like
        describing the system.
        The following gives the number of elements in the tuple and
        the interpretation:

        * 1 (instance of `lti`)
        * 2 (num, den)
        * 3 (zeros, poles, gain)
        * 4 (A, B, C, D)

    X0 : array_like, optional
        Initial state-vector (default is zero).
    T : array_like, optional
        Time points (computed if not given).
    N : int, optional
        Number of time points to compute if `T` is not given.

    Returns
    -------
    T : 1D ndarray
        Output time points.
    yout : 1D ndarray
        Step response of system.


    Notes
    -----
    If (num, den) is passed in for ``system``, coefficients for both the
    numerator and denominator should be specified in descending exponent
    order (e.g. ``s^2 + 3s + 5`` would be represented as ``[1, 3, 5]``).

    Examples
    --------
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> lti = signal.lti([1.0], [1.0, 1.0])
    >>> t, y = signal.step(lti)
    >>> plt.plot(t, y)
    >>> plt.xlabel('Time [s]')
    >>> plt.ylabel('Amplitude')
    >>> plt.title('Step response for 1. Order Lowpass')
    >>> plt.grid()

    """
    if isinstance(system, lti):
        sys = system._as_ss()
    elif isinstance(system, dlti):
        raise AttributeError('step can only be used with continuous-time '
                             'systems.')
    else:
        sys = lti(*system)._as_ss()
    if N is None:
        N = 100
    if T is None:
        T = _default_response_times(sys.A, N)
    else:
        T = asarray(T)
    U = ones(T.shape, sys.A.dtype)
    vals = lsim(sys, U, T, X0=X0, interp=False)
    return vals[0], vals[1]


def step(request):
    """step keyword argument for rolling window operations."""
    return request.param


def step(result: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return StepOp(result=result, loc=loc, ip=ip).result

