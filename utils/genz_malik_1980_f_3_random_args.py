
def genz_malik_1980_f_3_random_args(rng, shape, xp):
    alphas = xp.asarray(rng.random(shape))
    normalisation_factors = xp.sum(alphas, axis=-1)[..., None]
    difficulty = 12.0
    alphas = difficulty * alphas / normalisation_factors

    return (alphas,)

