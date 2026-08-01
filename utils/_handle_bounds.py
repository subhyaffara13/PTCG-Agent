
def _handle_bounds(bounds):
    # introduce auxiliary variables as needed for univariate
    # inequalities

    def _make_list(length: int, index_value_pairs):
        li = [0] * length
        for idx, val in index_value_pairs:
            li[idx] = val
        return li

    unbound = []
    row = []
    row2 = []
    b_len = len(bounds)
    for x, (a, b) in enumerate(bounds):
        if a is None and b is None:
            unbound.append(x)
        elif a is None:
            # r[x] = b - u
            b_len += 1
            row.append(_make_list(b_len, [(x, 1), (-1, 1)]))
            row.append(_make_list(b_len, [(x, -1), (-1, -1)]))
            row2.extend([[b], [-b]])
        elif b is None:
            if a:
                # r[x] = a + u
                b_len += 1
                row.append(_make_list(b_len, [(x, 1), (-1, -1)]))
                row.append(_make_list(b_len, [(x, -1), (-1, 1)]))
                row2.extend([[a], [-a]])
            else:
                # standard nonnegative relationship
                pass
        else:
            # r[x] = u + a
            b_len += 1
            row.append(_make_list(b_len, [(x, 1), (-1, -1)]))
            row.append(_make_list(b_len, [(x, -1), (-1, 1)]))
            # u <= b - a
            row.append(_make_list(b_len, [(-1, 1)]))
            row2.extend([[a], [-a], [b - a]])

    # make change of variables for unbound variables
    for x in unbound:
        # r[x] = u - v
        b_len += 2
        row.append(_make_list(b_len, [(x, 1), (-1, 1), (-2, -1)]))
        row.append(_make_list(b_len, [(x, -1), (-1, -1), (-2, 1)]))
        row2.extend([[0], [0]])

    return Matrix([r + [0]*(b_len - len(r)) for r in row]), Matrix(row2)

