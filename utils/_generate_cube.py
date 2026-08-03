import itertools

def _generate_cube():
    return np.array(list(itertools.product([-1, 1.], repeat=3)))

