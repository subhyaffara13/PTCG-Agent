
def assert_array_compare(
    comparison,
    x,
    y,
    err_msg="",
    verbose=True,
    header="",
    precision=6,
    equal_nan=True,
    equal_inf=True,
    *,
    strict=False,
):
    __tracebackhide__ = True  # Hide traceback for py.test
    from torch._numpy import all, array, asarray, bool_, inf, isnan, max

    x = asarray(x)
    y = asarray(y)

    def array2string(a):
        return str(a)

    # original array for output formatting
    ox, oy = x, y

    def func_assert_same_pos(x, y, func=isnan, hasval="nan"):
        """Handling nan/inf.

        Combine results of running func on x and y, checking that they are True
        at the same locations.

        """
        __tracebackhide__ = True  # Hide traceback for py.test
        x_id = func(x)
        y_id = func(y)
        # We include work-arounds here to handle three types of slightly
        # pathological ndarray subclasses:
        # (1) all() on `masked` array scalars can return masked arrays, so we
        #     use != True
        # (2) __eq__ on some ndarray subclasses returns Python booleans
        #     instead of element-wise comparisons, so we cast to bool_() and
        #     use isinstance(..., bool) checks
        # (3) subclasses with bare-bones __array_function__ implementations may
        #     not implement np.all(), so favor using the .all() method
        # We are not committed to supporting such subclasses, but it's nice to
        # support them if possible.
        if (x_id == y_id).all().item() is not True:
            msg = build_err_msg(
                [x, y],
                err_msg + f"\nx and y {hasval} location mismatch:",
                verbose=verbose,
                header=header,
                names=("x", "y"),
                precision=precision,
            )
            raise AssertionError(msg)
        # If there is a scalar, then here we know the array has the same
        # flag as it everywhere, so we should return the scalar flag.
        if isinstance(x_id, bool) or x_id.ndim == 0:
            return bool_(x_id)
        elif isinstance(y_id, bool) or y_id.ndim == 0:
            return bool_(y_id)
        else:
            return y_id

    try:
        if strict:
            cond = x.shape == y.shape and x.dtype == y.dtype
        else:
            cond = (x.shape == () or y.shape == ()) or x.shape == y.shape
        if not cond:
            if x.shape != y.shape:
                reason = f"\n(shapes {x.shape}, {y.shape} mismatch)"
            else:
                reason = f"\n(dtypes {x.dtype}, {y.dtype} mismatch)"
            msg = build_err_msg(
                [x, y],
                err_msg + reason,
                verbose=verbose,
                header=header,
                names=("x", "y"),
                precision=precision,
            )
            raise AssertionError(msg)

        flagged = bool_(False)

        if equal_nan:
            flagged = func_assert_same_pos(x, y, func=isnan, hasval="nan")

        if equal_inf:
            flagged |= func_assert_same_pos(
                x, y, func=lambda xy: xy == +inf, hasval="+inf"
            )
            flagged |= func_assert_same_pos(
                x, y, func=lambda xy: xy == -inf, hasval="-inf"
            )

        if flagged.ndim > 0:
            x, y = x[~flagged], y[~flagged]
            # Only do the comparison if actual values are left
            if x.size == 0:
                return
        elif flagged:
            # no sense doing comparison if everything is flagged.
            return

        val = comparison(x, y)

        if isinstance(val, bool):
            cond = val
            reduced = array([val])
        else:
            reduced = val.ravel()
            cond = reduced.all()

        # The below comparison is a hack to ensure that fully masked
        # results, for which val.ravel().all() returns np.ma.masked,
        # do not trigger a failure (np.ma.masked != True evaluates as
        # np.ma.masked, which is falsy).
        if not cond:
            n_mismatch = reduced.size - int(reduced.sum(dtype=intp))
            n_elements = flagged.size if flagged.ndim != 0 else reduced.size
            percent_mismatch = 100 * n_mismatch / n_elements
            remarks = [
                f"Mismatched elements: {n_mismatch} / {n_elements} ({percent_mismatch:.3g}%)"
            ]

            # with errstate(all='ignore'):
            # ignore errors for non-numeric types
            with contextlib.suppress(TypeError, RuntimeError):
                error = abs(x - y)
                if np.issubdtype(x.dtype, np.unsignedinteger):
                    error2 = abs(y - x)
                    np.minimum(error, error2, out=error)
                max_abs_error = max(error)
                remarks.append(
                    "Max absolute difference: " + array2string(max_abs_error.item())
                )

                # note: this definition of relative error matches that one
                # used by assert_allclose (found in np.isclose)
                # Filter values where the divisor would be zero
                nonzero = bool_(y != 0)
                if all(~nonzero):
                    max_rel_error = array(inf)
                else:
                    max_rel_error = max(error[nonzero] / abs(y[nonzero]))
                remarks.append(
                    "Max relative difference: " + array2string(max_rel_error.item())
                )

            err_msg += "\n" + "\n".join(remarks)
            msg = build_err_msg(
                [ox, oy],
                err_msg,
                verbose=verbose,
                header=header,
                names=("x", "y"),
                precision=precision,
            )
            raise AssertionError(msg)
    except ValueError:
        import traceback

        efmt = traceback.format_exc()
        header = f"error during assertion:\n\n{efmt}\n\n{header}"

        msg = build_err_msg(
            [x, y],
            err_msg,
            verbose=verbose,
            header=header,
            names=("x", "y"),
            precision=precision,
        )
        raise ValueError(msg)  # noqa: B904


def assert_array_compare(comparison, x, y, err_msg='', verbose=True, header='',
                         fill_value=True):
    """
    Asserts that comparison between two masked arrays is satisfied.

    The comparison is elementwise.

    """
    # Allocate a common mask and refill
    m = mask_or(getmask(x), getmask(y))
    x = masked_array(x, copy=False, mask=m, keep_mask=False, subok=False)
    y = masked_array(y, copy=False, mask=m, keep_mask=False, subok=False)
    if ((x is masked) and not (y is masked)) or \
            ((y is masked) and not (x is masked)):
        msg = build_err_msg([x, y], err_msg=err_msg, verbose=verbose,
                            header=header, names=('x', 'y'))
        raise ValueError(msg)
    # OK, now run the basic tests on filled versions
    return np.testing.assert_array_compare(comparison,
                                           x.filled(fill_value),
                                           y.filled(fill_value),
                                           err_msg=err_msg,
                                           verbose=verbose, header=header)


def assert_array_compare(comparison, x, y, err_msg='', verbose=True, header='',
                         precision=6, equal_nan=True, equal_inf=True,
                         *, strict=False, names=('ACTUAL', 'DESIRED')):
    __tracebackhide__ = True  # Hide traceback for py.test
    from numpy._core import all, array2string, errstate, inf, isnan, max, object_

    x = np.asanyarray(x)
    y = np.asanyarray(y)

    # original array for output formatting
    ox, oy = x, y

    def isnumber(x):
        return type(x.dtype)._is_numeric

    def istime(x):
        return x.dtype.char in "Mm"

    def isvstring(x):
        return x.dtype.char == "T"

    def robust_any_difference(x, y):
        # We include work-arounds here to handle three types of slightly
        # pathological ndarray subclasses:
        # (1) all() on fully masked arrays returns np.ma.masked, so we use != True
        #     (np.ma.masked != True evaluates as np.ma.masked, which is falsy).
        # (2) __eq__ on some ndarray subclasses returns Python booleans
        #     instead of element-wise comparisons, so we cast to np.bool() in
        #     that case (or in case __eq__ returns some other value with no
        #     all() method).
        # (3) subclasses with bare-bones __array_function__ implementations may
        #     not implement np.all(), so favor using the .all() method
        # We are not committed to supporting cases (2) and (3), but it's nice to
        # support them if possible.
        result = x == y
        if not hasattr(result, "all") or not callable(result.all):
            result = np.bool(result)
        return result.all() != True

    def func_assert_same_pos(x, y, func=isnan, hasval='nan'):
        """Handling nan/inf.

        Combine results of running func on x and y, checking that they are True
        at the same locations.

        """
        __tracebackhide__ = True  # Hide traceback for py.test

        x_id = func(x)
        y_id = func(y)
        if robust_any_difference(x_id, y_id):
            msg = build_err_msg(
                [x, y],
                err_msg + f'\n{hasval} location mismatch:',
                verbose=verbose, header=header,
                names=names,
                precision=precision)
            raise AssertionError(msg)
        # If there is a scalar, then here we know the array has the same
        # flag as it everywhere, so we should return the scalar flag.
        # np.ma.masked is also handled and converted to np.False_ (even if the other
        # array has nans/infs etc.; that's OK given the handling later of fully-masked
        # results).
        if isinstance(x_id, bool) or x_id.ndim == 0:
            return np.bool(x_id)
        elif isinstance(y_id, bool) or y_id.ndim == 0:
            return np.bool(y_id)
        else:
            return y_id

    def assert_same_inf_values(x, y, infs_mask):
        """
        Verify all inf values match in the two arrays
        """
        __tracebackhide__ = True  # Hide traceback for py.test

        if not infs_mask.any():
            return
        if x.ndim > 0 and y.ndim > 0:
            x = x[infs_mask]
            y = y[infs_mask]
        else:
            assert infs_mask.all()

        if robust_any_difference(x, y):
            msg = build_err_msg(
                [x, y],
                err_msg + '\ninf values mismatch:',
                verbose=verbose, header=header,
                names=names,
                precision=precision)
            raise AssertionError(msg)

    try:
        if strict:
            cond = x.shape == y.shape and x.dtype == y.dtype
        else:
            cond = (x.shape == () or y.shape == ()) or x.shape == y.shape
        if not cond:
            if x.shape != y.shape:
                reason = f'\n(shapes {x.shape}, {y.shape} mismatch)'
            else:
                reason = f'\n(dtypes {x.dtype}, {y.dtype} mismatch)'
            msg = build_err_msg([x, y],
                                err_msg
                                + reason,
                                verbose=verbose, header=header,
                                names=names,
                                precision=precision)
            raise AssertionError(msg)

        flagged = np.bool(False)
        if isnumber(x) and isnumber(y):
            if equal_nan:
                flagged = func_assert_same_pos(x, y, func=isnan, hasval='nan')

            if equal_inf:
                # If equal_nan=True, skip comparing nans below for equality if they are
                # also infs (e.g. inf+nanj) since that would always fail.
                isinf_func = lambda xy: np.logical_and(np.isinf(xy), np.invert(flagged))
                infs_mask = func_assert_same_pos(
                    x, y,
                    func=isinf_func,
                    hasval='inf')
                assert_same_inf_values(x, y, infs_mask)
                flagged |= infs_mask

        elif istime(x) and istime(y):
            # If one is datetime64 and the other timedelta64 there is no point
            if equal_nan and x.dtype.type == y.dtype.type:
                flagged = func_assert_same_pos(x, y, func=isnat, hasval="NaT")

        elif isvstring(x) and isvstring(y):
            dt = x.dtype
            if equal_nan and dt == y.dtype and hasattr(dt, 'na_object'):
                is_nan = (isinstance(dt.na_object, float) and
                          np.isnan(dt.na_object))
                bool_errors = 0
                try:
                    bool(dt.na_object)
                except TypeError:
                    bool_errors = 1
                if is_nan or bool_errors:
                    # nan-like NA object
                    flagged = func_assert_same_pos(
                        x, y, func=isnan, hasval=x.dtype.na_object)

        if flagged.ndim > 0:
            x, y = x[~flagged], y[~flagged]
            # Only do the comparison if actual values are left
            if x.size == 0:
                return
        elif flagged:
            # no sense doing comparison if everything is flagged.
            return

        val = comparison(x, y)
        invalids = np.logical_not(val)

        if isinstance(val, bool):
            cond = val
            reduced = array([val])
        else:
            reduced = val.ravel()
            cond = reduced.all()

        # The below comparison is a hack to ensure that fully masked
        # results, for which val.ravel().all() returns np.ma.masked,
        # do not trigger a failure (np.ma.masked != True evaluates as
        # np.ma.masked, which is falsy).
        if cond != True:
            n_mismatch = reduced.size - reduced.sum(dtype=intp)
            n_elements = flagged.size if flagged.ndim != 0 else reduced.size
            percent_mismatch = 100 * n_mismatch / n_elements
            remarks = [(f'Mismatched elements: {n_mismatch} / {n_elements} '
                        f'({percent_mismatch:.3g}%)')]
            if invalids.ndim != 0:
                if flagged.ndim > 0:
                    positions = np.argwhere(np.asarray(~flagged))[invalids]
                else:
                    positions = np.argwhere(np.asarray(invalids))
                s = "\n".join(
                    [
                        f" {p.tolist()}: {ox if ox.ndim == 0 else ox[tuple(p)]} "
                        f"({names[0]}), {oy if oy.ndim == 0 else oy[tuple(p)]} "
                        f"({names[1]})"
                        for p in positions[:5]
                    ]
                )
                if len(positions) == 1:
                    remarks.append(
                        f"Mismatch at index:\n{s}"
                    )
                elif len(positions) <= 5:
                    remarks.append(
                        f"Mismatch at indices:\n{s}"
                    )
                else:
                    remarks.append(
                        f"First 5 mismatches are at indices:\n{s}"
                    )

            with errstate(all='ignore'):
                # ignore errors for non-numeric types
                with contextlib.suppress(TypeError):
                    error = abs(x - y)
                    if np.issubdtype(x.dtype, np.unsignedinteger):
                        error2 = abs(y - x)
                        np.minimum(error, error2, out=error)

                    reduced_error = error[invalids]
                    max_abs_error = max(reduced_error)
                    if getattr(error, 'dtype', object_) == object_:
                        remarks.append(
                            'Max absolute difference among violations: '
                            + str(max_abs_error))
                    else:
                        remarks.append(
                            'Max absolute difference among violations: '
                            + array2string(max_abs_error))

                    # note: this definition of relative error matches that one
                    # used by assert_allclose (found in np.isclose)
                    # Filter values where the divisor would be zero
                    nonzero = np.bool(y != np.zeros_like(y))
                    nonzero_and_invalid = np.logical_and(invalids, nonzero)

                    if all(~nonzero_and_invalid):
                        max_rel_error = array(inf)
                    else:
                        nonzero_invalid_error = error[nonzero_and_invalid]
                        broadcasted_y = np.broadcast_to(y, error.shape)
                        nonzero_invalid_y = broadcasted_y[nonzero_and_invalid]
                        max_rel_error = max(nonzero_invalid_error
                                            / abs(nonzero_invalid_y))

                    if getattr(error, 'dtype', object_) == object_:
                        remarks.append(
                            'Max relative difference among violations: '
                            + str(max_rel_error))
                    else:
                        remarks.append(
                            'Max relative difference among violations: '
                            + array2string(max_rel_error))
            err_msg = str(err_msg)
            err_msg += '\n' + '\n'.join(remarks)
            msg = build_err_msg([ox, oy], err_msg,
                                verbose=verbose, header=header,
                                names=names,
                                precision=precision)
            raise AssertionError(msg)
    except ValueError:
        import traceback
        efmt = traceback.format_exc()
        header = f'error during assertion:\n\n{efmt}\n\n{header}'

        msg = build_err_msg([x, y], err_msg, verbose=verbose, header=header,
                            names=names, precision=precision)
        raise ValueError(msg)

