
def multi_scale_map(
    xs,
    ys,
    randomizer,
    scales=[(3, [0.2, 0.3]), (10, [0.1, 0.2]), (30, [0.05, 0.1]), (150, [0.01, 0.05])],
):
    gmap = np.zeros((xs, ys), dtype=np.int32)
    for scale in scales:
        n, lb = scale
        gmap = gen_map(xs, ys, n, randomizer, length_bounds=lb, gmap=gmap)
    return gmap

