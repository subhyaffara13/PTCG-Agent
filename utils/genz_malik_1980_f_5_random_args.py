import math


def genz_malik_1980_f_5_random_args(rng, shape, xp):
    alphas = xp.asarray(rng.random(shape))
    betas = xp.asarray(rng.random(shape))

    difficulty = 21.0
    normalisation_factors = xp.sqrt(xp.sum(alphas**xp.asarray(2.0), axis=-1))[..., None]
    alphas = alphas / normalisation_factors * math.sqrt(difficulty)

    return alphas, betas

