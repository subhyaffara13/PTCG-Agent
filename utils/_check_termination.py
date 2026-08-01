
def _check_termination(factors, n, limit, use_trial, use_rho, use_pm1,
                       verbose, next_p):
    """
    Helper function for integer factorization. Checks if ``n``
    is a prime or a perfect power, and in those cases updates the factorization.
    """
    if verbose:
        print('Check for termination')
    if n == 1:
        if verbose:
            print(complete_msg)
        return True
    if n < next_p**2 or isprime(n):
        factor_cache[n] = n
        factors[int(n)] = 1
        if verbose:
            print(complete_msg)
        return True

    # since we've already been factoring there is no need to do
    # simultaneous factoring with the power check
    p = _perfect_power(n, next_p)
    if not p:
        return False
    base, exp = p
    if base < next_p**2 or isprime(base):
        factor_cache[n] = base
        factors[base] = exp
    else:
        facs = factorint(base, limit, use_trial, use_rho, use_pm1,
                         verbose=False)
        for b, e in facs.items():
            if verbose:
                print(factor_msg % (b, e))
            factors[b] = exp*e
    if verbose:
        print(complete_msg)
    return True


def _check_termination(work, res, res_work_pairs, active, check_termination,
                       preserve_shape, xp):
    # Checks termination conditions, updates elements of `res` with
    # corresponding elements of `work`, and compresses `work`.

    stop = check_termination(work)

    if xp.any(stop):
        # update the active elements of the result object with the active
        # elements for which a termination condition has been met
        _update_active(work, res, res_work_pairs, active, stop, preserve_shape, xp)

        if preserve_shape:
            stop = stop[active]

        proceed = ~stop
        active = active[proceed]

        if not preserve_shape:
            # compress the arrays to avoid unnecessary computation
            for key, val in work.items():
                # `continued_fraction` hacks `n`; improve if this becomes a problem
                if key in {'args', 'n'}:
                    continue
                work[key] = val[proceed] if getattr(val, 'ndim', 0) > 0 else val
            work.args = [arg[proceed] for arg in work.args]

    return active

