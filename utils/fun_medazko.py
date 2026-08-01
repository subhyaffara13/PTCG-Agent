
def fun_medazko(t, y):
    n = y.shape[0] // 2
    k = 100
    c = 4

    phi = 2 if t <= 5 else 0
    y = np.hstack((phi, 0, y, y[-2]))

    d = 1 / n
    j = np.arange(n) + 1
    alpha = 2 * (j * d - 1) ** 3 / c ** 2
    beta = (j * d - 1) ** 4 / c ** 2

    j_2_p1 = 2 * j + 2
    j_2_m3 = 2 * j - 2
    j_2_m1 = 2 * j
    j_2 = 2 * j + 1

    f = np.empty(2 * n)
    f[::2] = (alpha * (y[j_2_p1] - y[j_2_m3]) / (2 * d) +
              beta * (y[j_2_m3] - 2 * y[j_2_m1] + y[j_2_p1]) / d ** 2 -
              k * y[j_2_m1] * y[j_2])
    f[1::2] = -k * y[j_2] * y[j_2_m1]

    return f

