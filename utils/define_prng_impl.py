import random
from typing import Callable

def define_prng_impl(*,
                     key_shape: Shape,
                     seed: Callable[[Array], Array],
                     split: Callable[[Array, Shape], Array],
                     random_bits: Callable[[Array, int, Shape], Array],
                     fold_in: Callable[[Array, int], Array],
                     name: str = '<unnamed>',
                     tag: str = '?') -> Hashable:
  return random.PRNGSpec(prng.PRNGImpl(
      key_shape, seed, split, random_bits, fold_in,
      name=name, tag=tag))

