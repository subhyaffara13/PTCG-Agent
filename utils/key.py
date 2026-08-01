
def key(k: str | Iterable[str]) -> Key:
    """Create a key from a string. When a list of string is given,
    it will create a dotted key.

    :Example:

    >>> doc = document()
    >>> doc.append(key('foo'), 1)
    >>> doc.append(key(['bar', 'baz']), 2)
    >>> print(doc.as_string())
    foo = 1
    bar.baz = 2
    """
    if isinstance(k, str):
        return SingleKey(k)
    keys = [SingleKey(_k) for _k in k]
    if len(keys) == 1:
        return keys[0]
    return DottedKey(keys)


def key(
    seed: int, impl: str = "philox4x32-10", device: torch.device | None = None
) -> torch.Tensor:
    r"""Create a PRNG key from a seed.

    A key is a tensor that encodes the state needed to deterministically
    produce random values. Keys are consumed by generation functions to produce
    reproducible random tensors without any global state. The internal
    representation of the key depends on the chosen PRNG algorithm.

    Args:
        seed (int): The seed value for the PRNG.
        impl (str): PRNG algorithm. Currently only ``"philox4x32-10"`` is
            supported.
        device (:class:`torch.device`, optional): The desired device for the
            returned key. Default: ``cpu``.

    Returns:
        A tensor representing the PRNG key.

    .. note::

        For the ``"philox4x32-10"`` algorithm, the key is a uint64 tensor of
        shape ``(2,)`` encoding a ``(seed, offset)`` pair. The offset determines
        the starting position in the Philox output stream.

    Example::

        >>> key = torch.func._random.key(42, device="cuda")  # doctest: +SKIP
    """
    if impl != "philox4x32-10":
        raise NotImplementedError(f"key() does not support PRNG impl '{impl}'")

    # (seed, offset)
    return torch.tensor([seed, 0], dtype=torch.uint64, device=device)


def key(seed: int | ArrayLike, *,
        impl: PRNGSpecDesc | None = None,
        dtype: KeyDTypeLike | None = None) -> Array:
  """Create a pseudo-random number generator (PRNG) key given an integer seed.

  The result is a scalar array containing a key, whose dtype indicates
  the default PRNG implementation, as determined by the optional
  ``dtype`` or ``impl`` argument or, otherwise, by the ``jax_default_prng_impl``
  config flag at the time when this function is called.

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.
    impl: optional string specifying the PRNG implementation (e.g.
      ``'threefry2x32'``). Deprecated in favor of ``dtype``.
    dtype: optional dtype or string name specifying the PRNG implementation
      (e.g. ``jax.random.key_dtype('threefry2x32')`` or ``'threefry2x32'``).

  Returns:
    A scalar PRNG key array, consumable by random functions as well as ``split``
    and ``fold_in``.
  """
  if dtype is not None:
    if impl is not None:
      raise ValueError(
          "Cannot specify both `impl` and `dtype` arguments to jax.random.key")
    impl = dtype
  return _key('key', seed, impl)

