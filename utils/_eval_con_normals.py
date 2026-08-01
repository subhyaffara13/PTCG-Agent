
def _eval_con_normals(C: NDArray, x: NDArray, cons: dict, m: int, meq: int):
    if m == 0:
        return

    if meq > 0:
        row = 0
        for con in cons['eq']:
            temp = np.atleast_2d(con['jac'](x, *con['args']))
            C[row:row + temp.shape[0], :] = temp
            row += temp.shape[0]

    if m > meq:
        row = meq
        for con in cons['ineq']:
            temp = np.atleast_2d(con['jac'](x, *con['args']))
            C[row:row + temp.shape[0], :] = temp
            row += temp.shape[0]

    return

