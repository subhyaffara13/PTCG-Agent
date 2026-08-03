import random

def set_rng_seed(seed=None):
    if seed is None:
        seed = SEED
    torch.manual_seed(seed)
    random.seed(seed)
    if TEST_NUMPY:
        np.random.seed(seed)

