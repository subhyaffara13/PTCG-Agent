
def _dense_difference(fun, x0, f0, h, use_one_sided, method, workers):
    m = f0.size
    n = x0.size
    nfev = 0

    # h should have same dtype as x0
    result_type = xp_result_type(x0, f0, force_floating=True, xp=np)
    # output dtype should be the same as df_dx
    J_transposed = np.empty((n, m), dtype=result_type)

    if method == '2-point':
        def x_generator2(x0, h):
            for i in range(n):
                # If copying isn't done then it's possible for different workers
                # to see the same values of x1. (At least that's what happened
                # when I used `multiprocessing.dummy.Pool`).
                # I also considered creating all the vectors at once, but that
                # means assembling a very large N x N array. It's therefore a
                # trade-off between N array copies or creating an NxN array.
                x1 = np.copy(x0)
                x1[i] = x0[i] + h[i]
                yield x1

        # only f_evals (numerator) needs parallelization, the denominator
        # (the step size) is fast to calculate.
        f_evals = workers(fun, x_generator2(x0, h))
        dx = [(x0[i] + h[i]) - x0[i] for i in range(n)]
        df = [f_eval - f0 for f_eval in f_evals]
        df_dx = [delf / delx for delf, delx in zip(df, dx)]
        nfev += len(df_dx)

    elif method == '3-point':
        def x_generator3(x0, h, use_one_sided):
            for i, one_sided in enumerate(use_one_sided):
                x1 = np.copy(x0)
                x2 = np.copy(x0)
                if one_sided:
                    x1[i] = x0[i] + h[i]
                    x2[i] = x0[i] + 2*h[i]
                else:
                    x1[i] = x0[i] - h[i]
                    x2[i] = x0[i] + h[i]
                yield x1
                yield x2

        # workers may return something like a list that needs to be turned
        # into an iterable (can't call `next` on a list)
        f_evals = iter(workers(fun, x_generator3(x0, h, use_one_sided)))
        gen = x_generator3(x0, h, use_one_sided)
        dx = list()
        df = list()
        for i, one_sided in enumerate(use_one_sided):
            l = next(gen)
            u = next(gen)

            f1 = next(f_evals)
            f2 = next(f_evals)
            if one_sided:
                dx.append(u[i] - x0[i])
                df.append(-3.0 * f0 + 4 * f1 - f2)
            else:
                dx.append(u[i] - l[i])
                df.append(f2 - f1)
        df_dx = [delf / delx for delf, delx in zip(df, dx)]
        nfev += 2 * len(df_dx)
    elif method == 'cs':
        def x_generator_cs(x0, h):
            for i in range(n):
                xc = x0.astype(complex, copy=True)
                xc[i] += h[i] * 1.j
                yield xc

        f_evals = iter(workers(fun, x_generator_cs(x0, h)))
        df_dx = [f1.imag / hi for f1, hi in zip(f_evals, h)]
        nfev += len(df_dx)
    else:
        raise RuntimeError("Never be here.")

    for i, v in enumerate(df_dx):
        J_transposed[i] = v

    if m == 1:
        J_transposed = np.ravel(J_transposed)

    return J_transposed.T, nfev

