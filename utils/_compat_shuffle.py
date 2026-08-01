
def _compat_shuffle(rng, input):
    """wrapper around rng.shuffle for python 2 compatibility reasons"""
    rng.shuffle(input)

