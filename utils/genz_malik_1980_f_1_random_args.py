
def genz_malik_1980_f_1_random_args(rng, shape, xp):
    r = xp.asarray(rng.random(shape[:-1]))
    alphas = xp.asarray(rng.random(shape))

    difficulty = 9
    normalisation_factors = xp.sum(alphas, axis=-1)[..., None]
    alphas = difficulty * alphas / normalisation_factors

    return (r, alphas)

