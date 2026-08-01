
def genz_malik_1980_f_4_random_args(rng, shape, xp):
    ndim = shape[-1]

    alphas = xp.asarray(rng.random(shape))
    normalisation_factors = xp.sum(alphas, axis=-1)[..., None]
    difficulty = 14.0
    alphas = (difficulty / ndim) * alphas / normalisation_factors

    return (alphas,)

