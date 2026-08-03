import random

def stateful_rng(seed: typing.ArrayLike | None = None, *,
                 impl: random.PRNGSpecDesc | None = None) -> StatefulPRNG:
  """
  Experimental stateful RNG with implicitly-updated state.

  This implements a stateful PRNG API similar to :func:`numpy.random.default_rng`.
  It is compatible with JAX transformations like :func:`~jax.jit` and others,
  with a few exceptions mentioned in the Notes below.

  .. note::

    This stateful PRNG API is a convenience wrapper around JAX's classic
    stateless, explicitly updated PRNG, described in :mod:`jax.random`.
    For performance-critical applications, it is recommended to use
    :func:`jax.random.key` with explicit random state semantics.

  For a discussion of design considerations for this API, refer to
  :ref:`stateful-randomness-jep`.

  Args:
    seed: an optional 64- or 32-bit integer used as the value of the key.
      This must be specified if the generator is instantiated within transformed
      code; when used at the top level of the program, it may be omitted in
      which case the RNG will be seeded using the default NumPy seeding.
    impl: optional string specifying the PRNG implementation (e.g.
      ``'threefry2x32'``)

  Returns:
    A :class:`~jax.experimental.random.StatefulPRNG` object, with methods for generating
    random values.

  Notes:
    The :class:`~jax.experimental.random.StatefulPRNG` object created by this method uses
    :func:`~jax.Ref` objects to allow implicit updates of state, and thus
    inherits some of its limitiations. For example:

    - :class:`StatefulPRNG` objects cannot be among the return values of functions
      wrapped in JIT or other JAX transformations. This means in particular
      they cannot be used as `carry` values for :func:`jax.lax.scan`,
      :func:`jax.lax.while_loop`, and other JAX control flow.
    - :class:`StatefulPRNG` objects cannot be used together with
      :func:`jax.checkpoint` or :func:`jax.remat`; in these cases it's best to
      use the :meth:`StatefulPRNG.key` method to produce a standard JAX PRNG key.

  Examples:
    >>> from jax.experimental import random
    >>> rng = random.stateful_rng(42)

    Repeated draws implicitly update the key:

    >>> rng.uniform()
    Array(0.5302608, dtype=float32)
    >>> rng.uniform()
    Array(0.72766423, dtype=float32)

    This also works under transformations like :func:`jax.jit`:

    >>> import jax
    >>> jit_uniform = jax.jit(rng.uniform)
    >>> jit_uniform()
    Array(0.6672406, dtype=float32)
    >>> jit_uniform()
    Array(0.3890121, dtype=float32)

    Keys can be generated directly if desired:

    >>> rng.key()
    Array((), dtype=key<fry>) overlaying:
    [2954079971 3276725750]
    >>> rng.key()
    Array((), dtype=key<fry>) overlaying:
    [2765691542  824333390]
  """
  if seed is None:
    if not core.trace_ctx.is_top_level():
      raise TypeError(
        "When used within transformed code, jax.experimental.random.stateful_rng()"
        " requires an explicit seed to be set.")
    entropy = np.random.SeedSequence().entropy
    assert isinstance(entropy, int)
    seed = np.int64(entropy & np.iinfo(np.int64).max)
  assert seed is not None
  return StatefulPRNG(
    _base_key=random.key(seed, impl=impl),
    _counter=ref.new_ref(0)
  )

