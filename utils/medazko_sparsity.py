
def medazko_sparsity(n):
    cols = []
    rows = []

    i = np.arange(n) * 2

    cols.append(i[1:])
    rows.append(i[1:] - 2)

    cols.append(i)
    rows.append(i)

    cols.append(i)
    rows.append(i + 1)

    cols.append(i[:-1])
    rows.append(i[:-1] + 2)

    i = np.arange(n) * 2 + 1

    cols.append(i)
    rows.append(i)

    cols.append(i)
    rows.append(i - 1)

    cols = np.hstack(cols)
    rows = np.hstack(rows)

    return coo_array((np.ones_like(cols), (cols, rows)))

