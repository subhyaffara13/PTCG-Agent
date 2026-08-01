
def _sparse_difference(fun, x0, f0, h, use_one_sided,
                       structure, groups, method, workers):
    m = f0.size
    n = x0.size
    row_indices = []
    col_indices = []
    fractions = []
    result_type = xp_result_type(x0, f0, force_floating=True, xp=np)

    n_groups = np.max(groups) + 1
    nfev = 0

    def e_generator():
        # Perturb variables which are in the same group simultaneously.
        for group in range(n_groups):
            yield np.equal(group, groups)

    def x_generator2():
        e_gen = e_generator()
        for e in e_gen:
            h_vec = h * e
            x = x0 + h_vec
            yield x

    def x_generator3():
        e_gen = e_generator()
        for e in e_gen:
            h_vec = h * e
            x1 = x0.copy()
            x2 = x0.copy()

            mask_1 = use_one_sided & e
            x1[mask_1] += h_vec[mask_1]
            x2[mask_1] += 2 * h_vec[mask_1]

            mask_2 = ~use_one_sided & e
            x1[mask_2] -= h_vec[mask_2]
            x2[mask_2] += h_vec[mask_2]
            yield x1
            yield x2

    def x_generator_cs():
        e_gen = e_generator()
        for e in e_gen:
            h_vec = h * e
            yield x0 + h_vec * 1.j

    # evaluate the function for each of the groups
    if method == '2-point':
        f_evals = iter(workers(fun, x_generator2()))
        xs = x_generator2()
    elif method == '3-point':
        f_evals = iter(workers(fun, x_generator3()))
        xs = x_generator3()
    elif method == 'cs':
        f_evals = iter(workers(fun, x_generator_cs()))

    for e in e_generator():
        # The result is written to columns which correspond to perturbed
        # variables.
        cols, = np.nonzero(e)
        # Find all non-zero elements in selected columns of Jacobian.
        i, j, _ = find(structure[:, cols])
        # Restore column indices in the full array.
        j = cols[j]

        if method == '2-point':
            dx = next(xs) - x0
            df = next(f_evals) - f0
            nfev += 1
        elif method == '3-point':
            # Here we do conceptually the same but separate one-sided
            # and two-sided schemes.
            x1 = next(xs)
            x2 = next(xs)

            mask_1 = use_one_sided & e
            mask_2 = ~use_one_sided & e

            dx = np.zeros(n, dtype=x0.dtype)
            dx[mask_1] = x2[mask_1] - x0[mask_1]
            dx[mask_2] = x2[mask_2] - x1[mask_2]

            f1 = next(f_evals)
            f2 = next(f_evals)
            nfev += 2

            mask = use_one_sided[j]
            df = np.empty(m, dtype=f0.dtype)

            rows = i[mask]
            df[rows] = -3 * f0[rows] + 4 * f1[rows] - f2[rows]

            rows = i[~mask]
            df[rows] = f2[rows] - f1[rows]
        elif method == 'cs':
            f1 = next(f_evals)
            nfev += 1
            df = f1.imag
            dx = h * e
        else:
            raise ValueError("Never be here.")

        # All that's left is to compute the fraction. We store i, j and
        # fractions as separate arrays and later construct csr_array.
        row_indices.append(i)
        col_indices.append(j)
        fractions.append(df[i] / dx[j])

    row_indices = np.hstack(row_indices)
    col_indices = np.hstack(col_indices)
    fractions = np.hstack(fractions)

    if isinstance(structure, spmatrix):
        return csr_matrix(
            (fractions, (row_indices, col_indices)),
            shape=(m, n),
            dtype=result_type
        ), nfev
    return csr_array(
        (fractions, (row_indices, col_indices)),
        shape=(m, n),
        dtype=result_type
    ), nfev

