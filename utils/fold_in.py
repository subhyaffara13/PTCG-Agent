
def fold_in(key: torch.Tensor, data: int) -> torch.Tensor:
    r"""Deterministically derive a new key by folding in an integer.

    Equivalent to ``split(key, data + 1)[data]``, but more efficient when
    only a single derived key is needed. Useful for associating a key with
    a loop iteration, layer index, or other integer identifier.

    Supports batched keys: if ``key`` has shape ``(*batch, K)``, each key in
    the batch is folded independently.

    Args:
        key (Tensor): A PRNG key returned by :func:`key`, :func:`split`, or
            :func:`fold_in`.
        data (int): An integer to fold into the key, interpreted as uint64.

    Returns:
        A new key tensor with the same shape as ``key``.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
        >>> k0 = torch.func._random.fold_in(key, 0)  # doctest: +SKIP
        >>> k1 = torch.func._random.fold_in(key, 1)  # doctest: +SKIP
        >>> # Equivalent to split:
        >>> keys = torch.func._random.split(key, 2)  # doctest: +SKIP
        >>> assert torch.equal(k0, keys[0])  # doctest: +SKIP
        >>> assert torch.equal(k1, keys[1])  # doctest: +SKIP
    """
    return torch.ops.aten._philox_key_fold_in(key, data)


def fold_in(key: ArrayLike, data: IntegerArray) -> Array:
  """Folds in data to a PRNG key to form a new PRNG key.

  Args:
    key: a PRNG key (from ``key``, ``split``, ``fold_in``).
    data: a 32-bit integer representing data to be folded into the key.

  Returns:
    A new PRNG key that is a deterministic function of the inputs and is
    statistically safe for producing a stream of new pseudo-random values.
  """
  key, wrapped = _check_prng_key("fold_in", key)
  if np.ndim(data):
    raise TypeError("fold_in accepts a scalar, but was given an array of"
                    f"shape {np.shape(data)} != (). Use jax.vmap for batching.")
  key_out = prng.random_fold_in(key, jnp.asarray(data, dtype='uint32'))
  return _return_prng_keys(wrapped, key_out)

