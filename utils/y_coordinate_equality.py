
def y_coordinate_equality(plot_data_func, evalf_func, system):
    """Checks whether the y-coordinate value of the plotted
    data point is equal to the value of the function at a
    particular x."""
    x, y = plot_data_func(system)
    x, y = _trim_tuple(x, y)
    y_exp = tuple(evalf_func(system, x_i) for x_i in x)
    return all(Abs(y_exp_i - y_i) < 1e-8 for y_exp_i, y_i in zip(y_exp, y))

