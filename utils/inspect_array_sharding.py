
def inspect_array_sharding(value, *, callback: Callable[[Sharding], None]):
  """Enables inspecting array sharding inside JIT-ted functions.

  This function, when provided with a Pytree of arrays, calls back with each of
  their shardings and works in ``jax.jit``-ted computations, enabling inspecting
  the chosen intermediate shardings.

  The policy for when ``callback`` is called is *as early as possible* when the
  sharding information is available. This means if ``inspect_array_callback`` is
  called without any transformations, the callback will happen immediately
  since we have the array and its sharding readily available. Inside of a
  ``jax.jit``, the callback will happen at lowering time, meaning you can
  trigger the callback using the AOT API (``jit(f).lower(...)``). When inside of
  a ``jax.jit``, the callback happens *at compile time* since the sharding is
  determined by XLA. You can trigger the callback by using JAX's AOT API
  (``jax.jit(f).lower(...).compile()``). In all cases, the callback will be
  triggered by running the function, since running a function entails lowering
  and compiling it first. However, once the function is compiled and cached,
  the callback will no longer occur.

  This function is experimental and its behavior may change in the future.

  Args:
    value: A Pytree of JAX arrays.
    callback: A callable that takes in a ``Sharding`` and doesn't return a value.

  In the following example, we print out the sharding of an intermediate value
  in a ``jax.jit``-ted computation:

  >>> import jax
  >>> import jax.numpy as jnp
  >>> from jax.sharding import Mesh, PartitionSpec
  >>>
  >>> x = jnp.arange(8, dtype=jnp.float32)
  >>> def f_(x):
  ...   x = jnp.sin(x)
  ...   jax.debug.inspect_array_sharding(x, callback=print)
  ...   return jnp.square(x)
  >>> f = jax.jit(f_, in_shardings=PartitionSpec('dev'),
  ...             out_shardings=PartitionSpec('dev'))
  >>> with jax.set_mesh(Mesh(jax.devices(), ('dev',))):
  ...   f.lower(x).compile()  # doctest: +SKIP
  ...
  NamedSharding(mesh={'dev': 8}, partition_spec=PartitionSpec(('dev',),))
  """
  def _inspect(val):
    inspect_sharding_p.bind(val, callback=callback)
  tree_util.tree_map(_inspect, value)

