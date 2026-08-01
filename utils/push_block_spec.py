
def push_block_spec(
    f: Callable,
    *in_spec_args,
    **in_spec_kwargs,
):
  def wrapper(*args, **kwargs):
    flat_block_specs, in_tree_ = tree_util.tree_flatten(
        (in_spec_args, in_spec_kwargs)
    )
    jaxpr, _, in_tree, out_tree = fuser_utils.make_jaxpr(f, *args, **kwargs)
    if in_tree != in_tree_:
      raise ValueError(f'Expected {in_tree} PyTree, got {in_tree_}')
    out_bs = _push_block_spec_jaxpr(jaxpr, *flat_block_specs)
    return tree_util.tree_unflatten(out_tree, out_bs)

  return wrapper

