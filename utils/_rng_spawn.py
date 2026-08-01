
def _rng_spawn(rng, n_children):
    # spawns independent RNGs from a parent RNG
    bg = rng._bit_generator
    ss = bg._seed_seq
    child_rngs = [np.random.Generator(type(bg)(child_ss))
                  for child_ss in ss.spawn(n_children)]
    return child_rngs

