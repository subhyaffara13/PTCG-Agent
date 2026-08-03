import math


def choice(a: ArrayLike, size=None, replace=True, p: ArrayLike | None = None):
    # https://stackoverflow.com/questions/59461811/random-choice-with-pytorch
    if a.numel() == 1:
        a = torch.arange(a)

    # TODO: check a.dtype is integer -- cf np.random.choice(3.4) which raises

    # number of draws
    if size is None:
        num_el = 1
    elif _util.is_sequence(size):
        num_el = 1
        for el in size:
            num_el *= el
    else:
        num_el = size

    # prepare the probabilities
    if p is None:
        p = torch.ones_like(a) / a.shape[0]

    # cf https://github.com/numpy/numpy/blob/main/numpy/random/mtrand.pyx#L973
    atol = sqrt(torch.finfo(p.dtype).eps)
    if abs(p.sum() - 1.0) > atol:
        raise ValueError("probabilities do not sum to 1.")

    # actually sample
    indices = torch.multinomial(p, num_el, replacement=replace)

    if _util.is_sequence(size):
        indices = indices.reshape(size)

    samples = a[indices]

    return samples


def choice(key: ArrayLike,
           a: int | ArrayLike,
           shape: Shape = (),
           replace: bool = True,
           p: RealArray | None = None,
           axis: int = 0,
           mode: str | None = None) -> Array:
  """Generates a random sample from a given array.

  .. warning::
    If ``p`` has fewer non-zero elements than the requested number of samples,
    as specified in ``shape``, and ``replace=False``, the output of this
    function is ill-defined. Please make sure to use appropriate inputs.

  Args:
    key: a PRNG key used as the random key.
    a : array or int. If an ndarray, a random sample is generated from
      its elements. If an int, the random sample is generated as if a were
      arange(a).
    shape : tuple of ints, optional. Output shape.  If the given shape is,
      e.g., ``(m, n)``, then ``m * n`` samples are drawn.  Default is (),
      in which case a single value is returned.
    replace : boolean.  Whether the sample is with or without replacement.
      Default is True.
    p : 1-D array-like, The probabilities associated with each entry in a.
      If not given the sample assumes a uniform distribution over all
      entries in a.
    axis: int, optional. The axis along which the selection is performed.
      The default, 0, selects by row.
    mode: optional, "high" or "low" for how many bits to use in the gumbel sampler
      when `p is None` and `replace = False`. The default is determined by the
      ``use_high_dynamic_range_gumbel`` config, which defaults to "low". With mode="low",
      in float32 sampling will be biased for choices with probability less than about
      1E-7; with mode="high" this limit is pushed down to about 1E-14. mode="high"
      approximately doubles the cost of sampling.

  Returns:
    An array of shape `shape` containing samples from `a`.
  """
  key, _ = _check_prng_key("choice", key)
  if not isinstance(shape, Sequence):
    raise TypeError("shape argument of jax.random.choice must be a sequence, "
                    f"got {shape}")
  check_arraylike("choice", a)
  arr = jnp.asarray(a)
  if arr.ndim == 0:
    n_inputs = core.concrete_or_error(int, a, "The error occurred in jax.random.choice()")
  else:
    axis = canonicalize_axis(axis, arr.ndim)
    n_inputs = arr.shape[axis]
  n_draws = math.prod(shape)
  if n_draws == 0:
    return jnp.zeros(shape, dtype=arr.dtype)
  if n_inputs <= 0:
    raise ValueError("a must be greater than 0 unless no samples are taken")
  if not replace and n_draws > n_inputs:
    raise ValueError(
        f"Cannot take a larger sample (size {n_draws}) than "
        f"population (size {n_inputs}) when 'replace=False'")

  if p is None:
    if replace:
      ind = randint(key, shape, 0, n_inputs)
      result = ind if arr.ndim == 0 else jnp.take(arr, ind, axis)
    else:
      slices = (slice(None),) * axis + (slice(n_draws),)
      result = permutation(key, n_inputs if arr.ndim == 0 else arr, axis)[slices]
  else:
    check_arraylike("choice", p)
    p_arr, = promote_dtypes_inexact(p)
    if p_arr.shape != (n_inputs,):
      raise ValueError(
          "p must be None or a 1D vector with the same size as a.shape[axis]. "
          f"p has shape {p_arr.shape} and a.shape[axis] is {n_inputs}.")
    if replace:
      p_cuml = jnp.cumsum(p_arr)
      r = p_cuml[-1] * (1 - uniform(key, shape, dtype=p_cuml.dtype))
      ind = jnp.searchsorted(p_cuml, r).astype(int)
    else:
      # Gumbel top-k trick: https://timvieira.github.io/blog/post/2019/09/16/algorithms-for-sampling-without-replacement/
      g = gumbel(key, (n_inputs,), dtype=p_arr.dtype, mode=mode) + jnp.log(p_arr)
      ind = lax.top_k(g, k=n_draws)[1].astype(int)
    result = ind if arr.ndim == 0 else jnp.take(arr, ind, axis)

  return result.reshape(shape if arr.ndim == 0 else
                        arr.shape[0:axis] + tuple(shape) + arr.shape[axis+1:])

