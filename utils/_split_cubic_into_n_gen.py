
def _split_cubic_into_n_gen(p0, p1, p2, p3, n):
    a, b, c, d = calc_cubic_parameters(p0, p1, p2, p3)
    dt = 1 / n
    delta_2 = dt * dt
    delta_3 = dt * delta_2
    for i in range(n):
        t1 = i * dt
        t1_2 = t1 * t1
        # calc new a, b, c and d
        a1 = a * delta_3
        b1 = (3 * a * t1 + b) * delta_2
        c1 = (2 * b * t1 + c + 3 * a * t1_2) * dt
        d1 = a * t1 * t1_2 + b * t1_2 + c * t1 + d
        yield calc_cubic_points(a1, b1, c1, d1)

