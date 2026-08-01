
def vectorstrength(events, period):
    '''
    Determine the vector strength of the events corresponding to the given
    period.

    The vector strength is a measure of phase synchrony, how well the
    timing of the events is synchronized to a single period of a periodic
    signal.

    If multiple periods are used, calculate the vector strength of each.
    This is called the "resonating vector strength".

    Parameters
    ----------
    events : 1D array_like
        An array of time points containing the timing of the events.
    period : float or array_like
        The period of the signal that the events should synchronize to.
        The period is in the same units as `events`.  It can also be an array
        of periods, in which case the outputs are arrays of the same length.

    Returns
    -------
    strength : float or 1D array
        The strength of the synchronization.  1.0 is perfect synchronization
        and 0.0 is no synchronization.  If `period` is an array, this is also
        an array with each element containing the vector strength at the
        corresponding period.
    phase : float or array
        The phase that the events are most strongly synchronized to in radians.
        If `period` is an array, this is also an array with each element
        containing the phase for the corresponding period.

    References
    ----------
    van Hemmen, JL, Longtin, A, and Vollmayr, AN. Testing resonating vector
        strength: Auditory system, electric fish, and noise.
        Chaos 21, 047508 (2011);
        :doi:`10.1063/1.3670512`.
    van Hemmen, JL.  Vector strength after Goldberg, Brown, and von Mises:
        biological and mathematical perspectives.  Biol Cybern.
        2013 Aug;107(4):385-96. :doi:`10.1007/s00422-013-0561-7`.
    van Hemmen, JL and Vollmayr, AN.  Resonating vector strength: what happens
        when we vary the "probing" frequency while keeping the spike times
        fixed.  Biol Cybern. 2013 Aug;107(4):491-94.
        :doi:`10.1007/s00422-013-0560-8`.
    '''
    xp = array_namespace(events, period)

    events = xp.asarray(events)
    period = xp.asarray(period)
    if xp.isdtype(period.dtype, 'integral'):
        period = xp.astype(period, xp.float64)

    if events.ndim > 1:
        raise ValueError('events cannot have dimensions more than 1')
    if period.ndim > 1:
        raise ValueError('period cannot have dimensions more than 1')

    # we need to know later if period was originally a scalar
    scalarperiod = not period.ndim

    events = xpx.atleast_nd(events, ndim=2, xp=xp)
    period = xpx.atleast_nd(period, ndim=2, xp=xp)
    if xp.any(period <= 0):
        raise ValueError('periods must be positive')

    # this converts the times to vectors
    events_ = xp.astype(events, period.dtype)
    vectors = xp.exp(2j * (xp.pi / period.T @ events_))

    # the vector strength is just the magnitude of the mean of the vectors
    # the vector phase is the angle of the mean of the vectors
    vectormean = xp.mean(vectors, axis=1)
    strength = xp.abs(vectormean)
    phase = _angle(vectormean, xp)

    # if the original period was a scalar, return scalars
    if scalarperiod:
        strength = strength[0]
        phase = phase[0]
    return strength, phase

