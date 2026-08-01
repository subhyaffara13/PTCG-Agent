
def _eval_matrix_sum(expression):
    f = expression.function
    for limit in expression.limits:
        i, a, b = limit
        dif = b - a
        if dif.is_Integer:
            if (dif < 0) == True:
                a, b = b + 1, a - 1
                f = -f

            newf = eval_sum_direct(f, (i, a, b))
            if newf is not None:
                return newf.doit()

