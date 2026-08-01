
def matrix(*args, **kwargs):
    return np.array(*args, **kwargs).view(np.matrix)

