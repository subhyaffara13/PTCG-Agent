
def _hypersphere_area(dim, radius):
    # https://en.wikipedia.org/wiki/N-sphere#Closed_forms
    return 2 * np.pi**(dim / 2) / gamma(dim / 2) * radius**(dim - 1)

