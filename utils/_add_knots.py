
def _add_knots(x, k, s, t, nmin, nmax,
               nest, fp, fpold,
               residuals, nplus):
    """
    Knot-growth helper for knot-finding loop (non-periodic).

    Parameters
    ----------
    x : 1-D ndarray
        Strictly increasing sample coordinates.
    k : int
        Spline degree.
    s : float
        Target smoothing.
    t : 1-D ndarray
        Current knot vector to be grown.
    nmin, nmax : int
        Lower/upper bounds on knot count (from initialisation).
    nest : int
        Storage cap for total knots.
    fp, fpold : float
        Current and previous residual sums of squares. Used to update nplus.
    residuals : 1-D ndarray
        Most recent residual signal used by `add_knot` to decide placement.
    nplus : int
        Previous iteration's proposed number of knots; used to update the next nplus.

    Returns
    -------
    t_new, nplus : tuple
        Updated knot vector and the nplus chosen for this step.
        If n >= nmax, t_new is a not-a-knot layout. If n >= nest, t_new is the
        current vector respecting the storage cap.

    What this function does
    -----------------------
    - Assumes the caller has already decided to GROW (i.e., checks
      like |fp - s| < acc or fp < s has FAILED).
    - Updates nplus (how many knots to add next) using the FITPACK heuristic
      based on the previous improvement (delta = fpold - fp).
    - Inserts up to nplus new internal knots using `add_knot(x, t, k, residuals)`.
    - Stops early if storage or interpolation caps are reached:
        * if n >= nmax: switch to interpolation layout (not-a-knot) and return
        * if n >= nest: return current t respecting storage cap

    How it compares with _fitpack_repro.py::_generate_knots_impl
    -------------------------------------------------------------
    Similarities:
      1) Same growth logic for nplus:
         - Use delta = fpold - fp with ratio fpms/delta
         - Apply min/max caps (doubling and halving behavior)
      3) Same storage guard:
         - If n reaches nest, stop and return current t
      4) Same end behavior at the "interpolating" cap:
         - When n >= nmax, switch to not-a-knot layout and return

    Differences:
      1) API style:
         - _generate_knots_impl is a generator that yields trial knot vectors and
           recomputes residuals/fp internally on each iteration.
         - `_add_knots` is a stateful helper that only grows knots; it expects the
           caller to handle residual computation and fp/fpold updates between calls.
      2) Periodicity:
         - _generate_knots_impl supports periodic=True.
         - `_add_knots` is non-periodic only; it uses not-a-knot when n >= nmax.
      3) Residual computation:
         - _generate_knots_impl calls an internal residual routine each iteration.
         - `_add_knots` does not compute residuals; the caller must supply:
             residuals (used by add_knot), fp, fpold.
      4) Return values:
         - _generate_knots_impl yields multiple t's and eventually returns None.
         - `_add_knots` returns:
             * (t_new, nplus) after inserting knots,
             * (not_a_knot_t, nplus) if n >= nmax,
             * (t, nplus) if n >= nest (storage cap).
    """

    acc = s * TOL
    n = t.size
    fpms = fp - s

    # ### c  increase the number of knots. ###

    # c  determine the number of knots nplus we are going to add.
    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L248-L261
    if n == nmin:
        nplus = 1
    else:
        delta = fpold - fp
        npl1 = int(nplus * fpms / delta) if delta > acc else nplus*2
        nplus = min(nplus*2, max(npl1, nplus//2, 1))

    # actually add knots
    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L271-L281
    # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L288-L295
    for j in range(nplus):
        t = add_knot(x, t, k, residuals)

        # check if we have enough knots already

        n = t.shape[0]
        # c  if n = nmax, sinf(x) is an interpolating spline.
        # c  if n=nmax we locate the knots as for interpolation.
        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L276-L279
        if n >= nmax:
            # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L93-L109
            # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L114-L131
            return _not_a_knot(x, k), nplus

        # c  if n=nest we cannot increase the number of knots because of
        # c  the storage capacity limitation.
        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L280
        # https://github.com/scipy/scipy/blob/v1.16.2/scipy/interpolate/fitpack/fpregr.f#L294
        if n >= nest:
            return t, nplus

    return t, nplus

