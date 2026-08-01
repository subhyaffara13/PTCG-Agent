
def nontrivial_problem():
    c = [-1, 8, 4, -6]
    A_ub = [[-7, -7, 6, 9],
            [1, -1, -3, 0],
            [10, -10, -7, 7],
            [6, -1, 3, 4]]
    b_ub = [-3, 6, -6, 6]
    A_eq = [[-10, 1, 1, -8]]
    b_eq = [-4]
    x_star = [101 / 1391, 1462 / 1391, 0, 752 / 1391]
    f_star = 7083 / 1391
    return c, A_ub, b_ub, A_eq, b_eq, x_star, f_star

