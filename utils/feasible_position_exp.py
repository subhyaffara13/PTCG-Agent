
def feasible_position_exp(randomizer, map_matrix, expanded_mat, constraints=None):
    """Returns a feasible position on map (map_matrix)."""
    xs, ys = map_matrix.shape
    while True:
        if constraints is None:
            x = randomizer.integers(0, xs)
            y = randomizer.integers(0, ys)
        else:
            xl, xu = constraints[0]
            yl, yu = constraints[1]
            x = randomizer.integers(xl, xu)
            y = randomizer.integers(yl, yu)
        if map_matrix[x, y] != -1 and expanded_mat[x + 1, y + 1] != -1:
            return (x, y)

