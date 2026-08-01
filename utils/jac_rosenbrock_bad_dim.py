
def jac_rosenbrock_bad_dim(x):
    return np.array([
        [-20 * x[0], 10],
        [-1, 0],
        [0.0, 0.0]
    ])

