
def _average_with_log_weights(x, logweights):
    x = np.asarray(x)
    logweights = np.asarray(logweights)
    maxlogw = logweights.max()
    weights = np.exp(logweights - maxlogw)
    return np.average(x, weights=weights)

