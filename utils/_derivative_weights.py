
def _derivative_weights(work, n, xp):
    # This produces the weights of the finite difference formula for a given
    # stencil. In experiments, use of a second-order central difference formula
    # with Richardson extrapolation was more accurate numerically, but it was
    # more complicated, and it would have become even more complicated when
    # adding support for one-sided differences. However, now that all the
    # function evaluation values are stored, they can be processed in whatever
    # way is desired to produce the derivative estimate. We leave alternative
    # approaches to future work. To be more self-contained, here is the theory
    # for deriving the weights below.
    #
    # Recall that the Taylor expansion of a univariate, scalar-values function
    # about a point `x` may be expressed as:
    #      f(x + h)  =     f(x) + f'(x)*h + f''(x)/2!*h**2  + O(h**3)
    # Suppose we evaluate f(x), f(x+h), and f(x-h).  We have:
    #      f(x)      =     f(x)
    #      f(x + h)  =     f(x) + f'(x)*h + f''(x)/2!*h**2  + O(h**3)
    #      f(x - h)  =     f(x) - f'(x)*h + f''(x)/2!*h**2  + O(h**3)
    # We can solve for weights `wi` such that:
    #   w1*f(x)      = w1*(f(x))
    # + w2*f(x + h)  = w2*(f(x) + f'(x)*h + f''(x)/2!*h**2) + O(h**3)
    # + w3*f(x - h)  = w3*(f(x) - f'(x)*h + f''(x)/2!*h**2) + O(h**3)
    #                =     0    + f'(x)*h + 0               + O(h**3)
    # Then
    #     f'(x) ~ (w1*f(x) + w2*f(x+h) + w3*f(x-h))/h
    # is a finite difference derivative approximation with error O(h**2),
    # and so it is said to be a "second-order" approximation. Under certain
    # conditions (e.g. well-behaved function, `h` sufficiently small), the
    # error in the approximation will decrease with h**2; that is, if `h` is
    # reduced by a factor of 2, the error is reduced by a factor of 4.
    #
    # By default, we use eighth-order formulae. Our central-difference formula
    # uses abscissae:
    #   x-h/c**3, x-h/c**2, x-h/c, x-h, x, x+h, x+h/c, x+h/c**2, x+h/c**3
    # where `c` is the step factor. (Typically, the step factor is greater than
    # one, so the outermost points - as written above - are actually closest to
    # `x`.) This "stencil" is chosen so that each iteration, the step can be
    # reduced by the factor `c`, and most of the function evaluations can be
    # reused with the new step size. For example, in the next iteration, we
    # will have:
    #   x-h/c**4, x-h/c**3, x-h/c**2, x-h/c, x, x+h/c, x+h/c**2, x+h/c**3, x+h/c**4
    # We do not reuse `x-h` and `x+h` for the new derivative estimate.
    # While this would increase the order of the formula and thus the
    # theoretical convergence rate, it is also less stable numerically.
    # (As noted above, there are other ways of processing the values that are
    # more stable. Thus, even now we store `f(x-h)` and `f(x+h)` in `work.fs`
    # to simplify future development of this sort of improvement.)
    #
    # The (right) one-sided formula is produced similarly using abscissae
    #   x, x+h, x+h/d, x+h/d**2, ..., x+h/d**6, x+h/d**7, x+h/d**7
    # where `d` is the square root of `c`. (The left one-sided formula simply
    # uses -h.) When the step size is reduced by factor `c = d**2`, we have
    # abscissae:
    #   x, x+h/d**2, x+h/d**3..., x+h/d**8, x+h/d**9, x+h/d**9
    # `d` is chosen as the square root of `c` so that the rate of the step-size
    # reduction is the same per iteration as in the central difference case.
    # Note that because the central difference formulas are inherently of even
    # order, for simplicity, we use only even-order formulas for one-sided
    # differences, too.

    # It's possible for the user to specify `fac` in, say, double precision but
    # `x` and `args` in single precision. `fac` gets converted to single
    # precision, but we should always use double precision for the intermediate
    # calculations here to avoid additional error in the weights.
    fac = float(work.fac)

    # Note that if the user switches back to floating point precision with
    # `x` and `args`, then `fac` will not necessarily equal the (lower
    # precision) cached `_derivative_weights.fac`, and the weights will
    # need to be recalculated. This could be fixed, but it's late, and of
    # low consequence.

    diff_state = work.diff_state
    if fac != diff_state.fac:
        diff_state.central = []
        diff_state.right = []
        diff_state.fac = fac

    if len(diff_state.central) != 2*n + 1:
        # Central difference weights. Consider refactoring this; it could
        # probably be more compact.
        # Note: Using NumPy here is OK; we convert to xp-type at the end
        i = np.arange(-n, n + 1)
        p = np.abs(i) - 1.  # center point has power `p` -1, but sign `s` is 0
        s = np.sign(i)

        h = s / fac ** p
        A = np.vander(h, increasing=True).T
        b = np.zeros(2*n + 1)
        b[1] = 1
        weights = np.linalg.solve(A, b)

        # Enforce identities to improve accuracy
        weights[n] = 0
        for i in range(n):
            weights[-i-1] = -weights[i]

        # Cache the weights. We only need to calculate them once unless
        # the step factor changes.
        diff_state.central = weights

        # One-sided difference weights. The left one-sided weights (with
        # negative steps) are simply the negative of the right one-sided
        # weights, so no need to compute them separately.
        i = np.arange(2*n + 1)
        p = i - 1.
        s = np.sign(i)

        h = s / np.sqrt(fac) ** p
        A = np.vander(h, increasing=True).T
        b = np.zeros(2 * n + 1)
        b[1] = 1
        weights = np.linalg.solve(A, b)

        diff_state.right = weights

    return (xp.asarray(diff_state.central, dtype=work.dtype),
            xp.asarray(diff_state.right, dtype=work.dtype))

