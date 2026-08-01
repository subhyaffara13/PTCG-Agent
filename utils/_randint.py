
def _randint(seed=None):
    """Return a randint generator.

    ``seed`` can be

    * None - return randomly seeded generator
    * int - return a generator seeded with the int
    * list - the values to be returned will be taken from the list
      in the order given; the provided list is not modified.

    Examples
    ========

    >>> from sympy.core.random import _randint
    >>> ri = _randint()
    >>> ri(1, 1000) # doctest: +SKIP
    999
    >>> ri = _randint(3)
    >>> ri(1, 1000) # doctest: +SKIP
    238
    >>> ri = _randint([0, 5, 1, 2, 4])
    >>> ri(1, 3), ri(1, 3)
    (1, 2)
    """
    if seed is None:
        return randint
    elif isinstance(seed, int):
        rng.seed(seed)
        return randint
    elif is_sequence(seed):
        seed = list(seed)  # make a copy
        seed.reverse()

        def give(a, b, seq=seed):
            a, b = as_int(a), as_int(b)
            w = b - a
            if w < 0:
                raise ValueError('_randint got empty range')
            try:
                x = seq.pop()
            except IndexError:
                raise ValueError('_randint sequence was too short')
            if a <= x <= b:
                return x
            else:
                return give(a, b, seq)
        return give
    else:
        raise ValueError('_randint got an unexpected seed')


def _randint(key, minval, maxval, shape, dtype) -> Array:
  # We have three imperfect options for generating random integers in an arbitrary
  # user-specified range:
  #
  # 1. Rejection sampling. This produces unbiased results, but involves a dynamic
  #    number of iterations, so it's not suitable for computation on accelerators.
  # 2. Generate floating point values between minval and maxval, and cast to int.
  #    This introduces bias for large ranges due to floating point rounding error:
  #    many integers within a given range would never be sampled.
  # 3. Generate numbers in a range that is a power of 2, and use an integer modulus
  #    to shift them into the desired range. This produces a biased distribution
  #    when the desired range is not a power of 2, which scales as
  #    O[bias] ~= (desired_range ** 2) / full_range.
  #
  # Given these three imperfect options, we opt for a modified version of (3), where we
  # sample 2 * nbits bits per value, because it is efficient and works well in most cases
  # of interest. To help users avoid inadvertently producing biased results, we always
  # generate samples in at least 32 bits.
  _check_shape("randint", shape, np.shape(minval), np.shape(maxval))
  if not dtypes.issubdtype(dtype, np.integer):
    raise TypeError(f"randint only accepts integer dtypes, got {dtype}")

  check_arraylike("randint", minval, maxval)
  minval = jnp.asarray(minval)
  maxval = jnp.asarray(maxval)
  if not dtypes.issubdtype(minval.dtype, np.integer):
    minval = minval.astype(int)
  if not dtypes.issubdtype(maxval.dtype, np.integer):
    maxval = maxval.astype(int)

  # Flag where maxval is greater than the maximum value of dtype
  # in order to handle cases like randint(key, shape, 0, 256, 'uint8')
  maxval_out_of_range = lax.gt(
    maxval, _convert_and_clip_integer(jnp.array(dtypes.iinfo(dtype).max, dtype), maxval.dtype))

  minval = _convert_and_clip_integer(minval, dtype)
  maxval = _convert_and_clip_integer(maxval, dtype)
  minval = lax.broadcast_to_rank(minval, len(shape))
  maxval = lax.broadcast_to_rank(maxval, len(shape))
  nbits = dtypes.iinfo(dtype).bits

  if nbits not in (8, 16, 32, 64):
    raise TypeError(f"randint only accepts 8-, 16-, 32-, or 64-bit dtypes, got {dtype}")

  # This algorithm is biased whenever (maxval - minval) is not a power of 2.
  # We generate double the number of random bits required by the dtype so as to
  # reduce that bias.
  k1, k2 = _split(key)
  rbits = lambda key: _random_bits(key, nbits, shape)
  higher_bits, lower_bits = rbits(k1), rbits(k2)

  unsigned_dtype = UINT_DTYPES[nbits]
  span = lax.convert_element_type(maxval - minval, unsigned_dtype)

  # Ensure that span=1 when maxval <= minval, so minval is always returned;
  # https://github.com/jax-ml/jax/issues/222
  span = lax.select(maxval <= minval, lax.full_like(span, 1), span)

  # When maxval is out of range, the span has to be one larger.
  # If span is already the maximum representable value, this will wrap to zero,
  # causing remainders below to have no effect, which is the correct semantics.
  span = lax.select(
    maxval_out_of_range & (maxval > minval),
    lax.add(span, lax._const(span, 1)),
    span)

  # To compute a remainder operation on an integer that might have twice as many
  # bits as we can represent in the native unsigned dtype, we compute a
  # multiplier equal to 2**nbits % span. To avoid overflow, we use the identity:
  #  (a * b) % N = [(a % N) * (b % N)] % N
  multiplier = lax.rem(lax._const(span, 2 ** (nbits // 2)), span)
  multiplier = lax.rem(lax.mul(multiplier, multiplier), span)

  random_offset = lax.add(lax.mul(lax.rem(higher_bits, span), multiplier),
                          lax.rem(lower_bits, span))
  random_offset = lax.rem(random_offset, span)
  return lax.add(minval, lax.convert_element_type(random_offset, dtype))

