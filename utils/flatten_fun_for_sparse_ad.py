import itertools
from typing import Any

def flatten_fun_for_sparse_ad(fun, argnums: int | tuple[int, ...], args: tuple[Any, ...]):
  argnums_tup = _ensure_index_tuple(argnums)
  assert all(0 <= argnum < len(args) for argnum in argnums_tup)

  # We do a two-step flattening to figure out how argnums maps to args_flat.
  # First, flatten arguments to a list containing sparse and dense objects.
  args_flat1, tree1 = tree_util.tree_flatten(args, is_leaf=is_sparse)
  *leaf_argnums1, end = split_list(range(tree1.num_leaves),
                                   [child.num_leaves for child in tree1.children()])
  assert not end
  argnums_flat1 = list(itertools.chain.from_iterable(
      nums for i, nums in enumerate(leaf_argnums1) if i in argnums_tup))

  # Next, fully flatten to a list of dense buffers.
  args_flat, tree2 = tree_util.tree_flatten(args_flat1)
  *leaf_argnums2, end = split_list(range(tree2.num_leaves),
                                   [child.num_leaves for child in tree2.children()])
  assert not end
  # For sparse args, we only mark the first buffer (the data) for differentiation.
  leaf_argnums2 = [nums[:1] if is_sparse(arg) else nums
                   for arg, nums in safe_zip(args_flat1, leaf_argnums2)]
  argnums_flat = tuple(itertools.chain.from_iterable(
      nums for i, nums in enumerate(leaf_argnums2) if i in argnums_flat1))

  def fun_flat(*args_flat, **kwargs):
    args = tree_util.tree_unflatten(tree1, tree_util.tree_unflatten(tree2, args_flat))
    return fun(*args, **kwargs)

  def reconstruct(i, grad_out):
    bufs, tree = tree_util.tree_flatten(args_flat1[i])
    f_recons = lambda g: tree_util.tree_unflatten(tree, [g, *bufs[1:]])
    for _ in range(grad_out.ndim - bufs[0].ndim):
      f_recons = jax.vmap(f_recons)
    return f_recons(grad_out)

  def postprocess_gradients(grads_out):
    leaf_grads = [None] * tree1.num_leaves
    for i, grad in safe_zip(argnums_flat1, grads_out):
      leaf_grads[i] = reconstruct(i, grad)
    grad_tree = tree_util.tree_unflatten(tree1, leaf_grads)
    grad_tree = tuple(filter(lambda x: jax.tree.leaves(x), grad_tree))
    return grad_tree[0] if len(grad_tree) == 1 else grad_tree

  return fun_flat, argnums_flat, args_flat, postprocess_gradients

