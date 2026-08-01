
def _generate_prism(n, axis):
    thetas = np.linspace(0, 2 * np.pi, n + 1)[:-1]
    bottom = np.vstack([-np.ones(n), np.cos(thetas), np.sin(thetas)]).T
    top = np.vstack([+np.ones(n), np.cos(thetas), np.sin(thetas)]).T
    P = np.concatenate((bottom, top))
    return np.roll(P, axis, axis=1)

