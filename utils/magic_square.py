
def magic_square(n, rng=None):
    """
    Generates a linear program for which integer solutions represent an
    n x n magic square; binary decision variables represent the presence
    (or absence) of an integer 1 to n^2 in each position of the square.
    """

    rng = np.random.default_rng(92350948245690509234) if rng is None else rng
    M = n * (n**2 + 1) / 2

    numbers = np.arange(n**4) // n**2 + 1

    numbers = numbers.reshape(n**2, n, n)

    zeros = np.zeros((n**2, n, n))

    A_list = []
    b_list = []

    # Rule 1: use every number exactly once
    for i in range(n**2):
        A_row = zeros.copy()
        A_row[i, :, :] = 1
        A_list.append(A_row.flatten())
        b_list.append(1)

    # Rule 2: Only one number per square
    for i in range(n):
        for j in range(n):
            A_row = zeros.copy()
            A_row[:, i, j] = 1
            A_list.append(A_row.flatten())
            b_list.append(1)

    # Rule 3: sum of rows is M
    for i in range(n):
        A_row = zeros.copy()
        A_row[:, i, :] = numbers[:, i, :]
        A_list.append(A_row.flatten())
        b_list.append(M)

    # Rule 4: sum of columns is M
    for i in range(n):
        A_row = zeros.copy()
        A_row[:, :, i] = numbers[:, :, i]
        A_list.append(A_row.flatten())
        b_list.append(M)

    # Rule 5: sum of diagonals is M
    A_row = zeros.copy()
    A_row[:, range(n), range(n)] = numbers[:, range(n), range(n)]
    A_list.append(A_row.flatten())
    b_list.append(M)
    A_row = zeros.copy()
    A_row[:, range(n), range(-1, -n - 1, -1)] = \
        numbers[:, range(n), range(-1, -n - 1, -1)]
    A_list.append(A_row.flatten())
    b_list.append(M)

    A = np.array(np.vstack(A_list), dtype=float)
    b = np.array(b_list, dtype=float)
    c = rng.random(A.shape[1])

    return A, b, c, numbers, M

