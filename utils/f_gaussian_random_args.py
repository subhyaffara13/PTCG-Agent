
def f_gaussian_random_args(rng, shape, xp):
    alphas = xp.asarray(rng.random(shape))

    # If alphas are very close to 0 this makes the problem very difficult due to large
    # values of ``f``.
    alphas *= 100

    return (alphas,)

