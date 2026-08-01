
def pad_shard_unpad(
  wrapped, static_argnums=(0,), static_argnames=(), static_return=False
):
  """Wraps a function with code that pads, shards, then un-shards, un-pads.

  Args:
    wrapped: the function to be wrapped. Signature is ``params, *args, *kwargs``.
    static_argnums: indices of arguments to ``wrapped`` that should _not_ be
      padded and sharded, but instead be forwarded as-is. The default is (0,)
      because by far the most common use-case is to pass ``params`` first.
    static_argnames: names of kwargs to ``wrapped`` that should _not_ be padded
      and sharded, but instead be forwarded as-is.
    static_return: whether not to un-shard, and un-pad the return value; static
      return values are typically used with eval steps that compute metrics

  Returns:
    A new function that pads and shards its arguments before passing them to
    the wrapped function, and un-shards and un-pads the returned pytree.

    This is useful for calling a pmap'ed function with inputs that aren't
    divisible by the number of devices. A typical use is:
      @pad_shard_unpad
      @jax.pmap
      def forward(params, x): ...

  Notes:
    The padding is done in host-memory before being passed to the function, and
    the values returned by the function are transferred back to host memory.

    The returned function is augmented with a new keyword-only argument
    ``min_device_batch`` that, if specified, forces padding inputs to at least
    this size per device. This can be useful to avoid recompiles for the last
    batch and reduce memory fragmentation.

    For more information refer to https://flax.readthedocs.io/en/latest/guides/data_preprocessing/full_eval.html
  """

  def pad_shard_unpad_wrapper(*args, min_device_batch=None, **kw):
    d = jax.local_device_count()  # d = devices, b = batch
    batch_sizes = set()
    for i, a in enumerate(args):
      if i not in static_argnums:
        batch_sizes |= {t.shape[0] for t in jax.tree_util.tree_leaves(a)}
    for k, v in kw.items():
      if k not in static_argnames:
        batch_sizes |= {t.shape[0] for t in jax.tree_util.tree_leaves(v)}
    assert len(batch_sizes) == 1, f'Inconsistent batch-sizes: {batch_sizes}'
    b = batch_sizes.pop()

    def pad(x):
      _, *shape = x.shape
      db, rest = divmod(b, d)
      if rest:
        x = np.concatenate([x, np.zeros((d - rest, *shape), x.dtype)], axis=0)
        db += 1
      if min_device_batch and db < min_device_batch:
        x = np.concatenate(
          [x, np.zeros((d * (min_device_batch - db), *shape), x.dtype)]
        )
        db = min_device_batch
      return x.reshape(d, db, *shape)

    def maybe_pad(tree, actually_pad=True):
      if not actually_pad:
        return tree  # For call-site convenience below.
      return jax.tree_util.tree_map(pad, tree)

    args = [maybe_pad(a, i not in static_argnums) for i, a in enumerate(args)]
    kw = {k: maybe_pad(v, k not in static_argnames) for k, v in kw.items()}
    out = wrapped(*args, **kw)

    def unpad(x):
      # Transfer back before cutting, to reduce on-device shape diversity.
      return jax.device_get(x).reshape([np.prod(x.shape[:2]), *x.shape[2:]])[:b]

    return out if static_return else jax.tree_util.tree_map(unpad, out)

  return pad_shard_unpad_wrapper

