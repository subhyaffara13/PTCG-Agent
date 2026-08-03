import math


def genz_malik_1980_f_2_random_args(rng, shape, xp):
    ndim = shape[-1]
    alphas = xp.asarray(rng.random(shape))
    betas = xp.asarray(rng.random(shape))

    difficulty = 25.0
    products = xp.prod(alphas**xp.asarray(-2.0), axis=-1)
    normalisation_factors = (products**xp.asarray(1 / (2*ndim)))[..., None]
    alphas = alphas * normalisation_factors * math.pow(difficulty, 1 / (2*ndim))

    # Adjust alphas from distribution used in Genz and Malik 1980 since denominator
    # is very small for high dimensions.
    alphas *= 10

    return alphas, betas

