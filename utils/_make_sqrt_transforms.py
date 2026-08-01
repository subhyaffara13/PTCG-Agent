
def _make_sqrt_transforms() -> TransFuncs:

    def sqrt(x):
        return np.sign(x) * np.sqrt(np.abs(x))

    def square(x):
        return np.sign(x) * np.square(x)

    return sqrt, square

