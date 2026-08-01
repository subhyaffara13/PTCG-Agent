
def shard_alike(x, y):
  """Shards x and y alike."""
  x_flat, x_tree = tree_flatten(x)
  y_flat, y_tree = tree_flatten(y)

  if x_tree != y_tree:
    raise ValueError('Trees should be equal. '
                     f'Got x_tree: {x_tree}, y_tree: {y_tree}')

  for x_, y_ in safe_zip(x_flat, y_flat):
    x_aval = core.shaped_abstractify(x_)
    y_aval = core.shaped_abstractify(y_)
    if x_aval.shape != y_aval.shape:
      raise ValueError(
          'The leaves shapes of `x` and `y` should match. Got `x` leaf shape:'
          f' {x_aval.shape} and `y` leaf shape: {y_aval.shape}. File an issue at'
          ' https://github.com/jax-ml/jax/issues if you want this feature.')

  outs = [shard_alike_p.bind(x_, y_) for x_, y_ in safe_zip(x_flat, y_flat)]
  x_out_flat, y_out_flat = zip(*outs)
  return tree_unflatten(x_tree, x_out_flat), tree_unflatten(y_tree, y_out_flat)

