
def sol_event_dense_output_LSODA(t):
    return np.exp(t ** 2 / 2 - 2 * t + np.log(0.05) - 6)

