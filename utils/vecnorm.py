
def vecnorm(x, ord=2):
    if ord == np.inf:
        return np.amax(np.abs(x))
    elif ord == -np.inf:
        return np.amin(np.abs(x))
    else:
        return np.sum(np.abs(x)**ord, axis=0)**(1.0 / ord)

