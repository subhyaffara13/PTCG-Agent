
def add_rectangle(input_map, xc, yc, xl, yl):
    """Add a rectangle to the input map.

    centered a xc, yc with dimensions xl, yl.
    Input specs are normalized wrt the map.
    """
    assert len(input_map.shape) == 2, "input_map must be a numpy matrix"

    xs, ys = input_map.shape
    xcc, ycc = int(round(xs * xc)), int(round(ys * yc))
    xll, yll = int(round(xs * xl)), int(round(ys * yl))
    if xll <= 1:
        x_lbound, x_upbound = xcc, xcc + 1
    else:
        x_lbound, x_upbound = xcc - xll / 2, xcc + xll / 2
    if yll <= 1:
        y_lbound, y_upbound = ycc, ycc + 1
    else:
        y_lbound, y_upbound = ycc - yll / 2, ycc + yll / 2

    # assert x_lbound >= 0 and x_upbound < xs, "Invalid rectangel config, x out of bounds"
    # assert y_lbound >= 0 and y_upbound < ys, "Invalid rectangel config, y out of bounds"

    x_lbound, x_upbound = np.clip([x_lbound, x_upbound], 0, xs)
    y_lbound, y_upbound = np.clip([y_lbound, y_upbound], 0, ys)

    for i in range(x_lbound, x_upbound):
        for j in range(y_lbound, y_upbound):
            input_map[j, i] = -1
    return input_map

