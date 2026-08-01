
def _generate_pyramid(n, axis):
    thetas = np.linspace(0, 2 * np.pi, n + 1)[:-1]
    P = np.vstack([np.zeros(n), np.cos(thetas), np.sin(thetas)]).T
    P = np.concatenate((P, [[1, 0, 0]]))
    return np.roll(P, axis, axis=1)

