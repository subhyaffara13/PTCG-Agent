
def per_example_layer_norm_clip(
    grads: base.ArrayTree,
    global_l2_norm_clip: jax.typing.ArrayLike,  # float
    uniform: bool = True
) -> tuple[base.ArrayTree, base.ArrayTree]:
  """Applies gradient clipping per-example using per-layer norms.

  If len(grads) == 1, this function is equivalent to
  optax.per_example_global_norm_clip.  If len(grads) > 1, each array in grads
  will be independently clipped to a value ``C_i`` documented below.

  Let ``C = global_l2_norm_clip value``. Then per-layer clipping is done as
  follows:

  1. If ``uniform`` is ``True``, each of the ``K`` layers has an individual clip
  norm of ``C / sqrt(K)``.

  2. If ``uniform`` is ``False``, each of the ``K`` layers has an individual
  clip norm of ``C * sqrt(D_i / D)`` where ``D_i`` is the number of parameters
  in layer ``i``, and ``D`` is the total number of parameters in the model.

  Args:
    grads: flattened update; i.e. a list of gradients in which each item is the
      gradient for one layer; the function expects these to have a batch
      dimension on the 0th axis.
    global_l2_norm_clip: overall L2 clip norm to use.
    uniform: If `True`, per-layer clip norm is ``global_l2_norm_clip/sqrt(L)``,
      where ``L`` is the number of layers. Otherwise, per-layer clip norm is
      ``global_l2_norm_clip * sqrt(f)``, where ``f`` is the fraction of total
      model parameters that are in this layer.

  Returns:
    A tuple containing sum of the clipped per-example grads and the number of
    per-example grads that were clipped for each layer.

  Example:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> grads = [jnp.array([[0, 0, 0], [0, 3, 4], [4, 0, 3], [3, 4, 0]])]
    >>> optax.per_example_layer_norm_clip(grads, jnp.inf)
    ([Array([7., 7., 7.], dtype=float32)], [Array(0, dtype=int32)])
    >>> optax.per_example_layer_norm_clip(grads, 0.0)
    ([Array([0., 0., 0.], dtype=float32)], [Array(3, dtype=int32)])
    >>> optax.per_example_layer_norm_clip(grads, 1.25)
    ([Array([1.75, 1.75, 1.75], dtype=float32)], [Array(3, dtype=int32)])

  References:
    McMahan et al., `Learning Differentially Private Recurrent Language Models
    <https://arxiv.org/abs/1710.06963>`_, 2017
  """

  if not _check_arrays_have_batch_dim(grads):
    raise ValueError(
        "Unlike other transforms, `per_example_layer_norm_clip` expects"
        " `grads` to have a batch dimension in the 0th axis; got shapes:"
        f" {jax.tree.map(jnp.shape, grads)}."
    )

  # Compute per-layer clip norms, based on whether we are using uniform
  # variant or not.
  if uniform:
    # Create list of length `num_layers` of per-layer clip norm.
    num_layers = len(jax.tree.leaves(grads))
    layer_clip_norms = jax.tree.map(
        lambda _: global_l2_norm_clip * (1.0 / num_layers) ** 0.5, grads
    )
  else:
    total_params = jax.tree.reduce(lambda x, g: x + g[0].size, grads, 0)
    layer_clip_norms = jax.tree.map(
        lambda g: global_l2_norm_clip * (g[0].size / total_params) ** 0.5,
        grads,
    )

  result = jax.tree.map(per_example_global_norm_clip, grads, layer_clip_norms)
  return jax.tree.transpose(
      outer_treedef=jax.tree.structure(grads),
      inner_treedef=jax.tree.structure((0, 0)),
      pytree_to_transpose=result,
  )

