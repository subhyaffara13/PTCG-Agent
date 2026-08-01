
def PRNGKey(seed: int | ArrayLike, *,
            impl: PRNGSpecDesc | None = None) -> Array:
  """Create a legacy PRNG key given an integer seed.

  This function produces old-style legacy PRNG keys, which are arrays
  of dtype ``uint32``. For more, see the note in the `PRNG keys
  <https://docs.jax.dev/en/latest/jax.random.html#prng-keys>`_
  section. When possible, :func:`jax.random.key` is recommended for
  use instead.

  The resulting key does not carry a PRNG implementation. The returned
  key matches the implementation given by the optional ``impl``
  argument or, otherwise, determined by the ``jax_default_prng_impl``
  config flag. Callers must ensure that same implementation is set as
  the default when passing this key as an argument to other functions
  (such as ``jax.random.split`` and ``jax.random.normal``).

  Args:
    seed: a 64- or 32-bit integer used as the value of the key.
    impl: optional string specifying the PRNG implementation (e.g.
      ``'threefry2x32'``)

  Returns:
    A PRNG key, consumable by random functions as well as ``split``
    and ``fold_in``.
  """
  return _return_prng_keys(True, _key('PRNGKey', seed, impl))

