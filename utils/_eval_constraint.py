
def _eval_constraint(d: NDArray, x: NDArray, cons: dict, m: int, meq: int):
    if m == 0:
        return

    # The reason why we don't use regular increments with a sane for loop is that
    # the constraint evaluations do not necessarily return scalars. Their
    # output length needs to be taken into account while placing them in d.

    if meq > 0:
        row = 0
        for con in cons['eq']:
            temp = np.atleast_1d(con['fun'](x, *con['args'])).ravel()
            d[row:row + len(temp)] = temp
            row += len(temp)

    if m > meq:
        row = meq
        for con in cons['ineq']:
            temp = np.atleast_1d(con['fun'](x, *con['args'])).ravel()
            d[row:row + len(temp)] = temp
            row += len(temp)

    return

