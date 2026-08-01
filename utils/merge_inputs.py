
def merge_inputs(
  *,
  ctxtag: str = 'split_merge_inputs',
) -> tp.Callable[[F], F]: ...


def merge_inputs(
  f: F,
  *,
  ctxtag: str = 'split_merge_inputs',
) -> F: ...


def merge_inputs(
  f: F | Missing = MISSING,
  *,
  ctxtag: str = 'split_merge_inputs',
) -> F | tp.Callable[[F], F]:
  """Takes in a function that contains jax-compatible data structures in the
  inputs and outputs, and returns a function that replaces the jax-compatible
  data structures the corresponding graph nodes. Must be used in conjunction
  with :func:`split_inputs`.

  Args:
    f: The function to be transformed.
    ctxtag: The context tag to be used for the transformation. Defaults to
      'split_merge_inputs'.

  Returns:
    The transformed function.

  For more information and examples, see :func:`split_inputs`.
  """
  if isinstance(f, Missing):
    return functools.partial(merge_inputs, ctxtag=ctxtag)  # type: ignore[return-value]

  @functools.wraps(f)
  def merge_inputs_wrapper(*pure_args):
    args = extract.from_tree(pure_args, ctxtag=ctxtag, is_inner=True)
    out = f(*args)
    args_out = extract.clear_non_graph_nodes(args)
    pure_args_out, pure_out = extract.to_tree((args_out, out), ctxtag=ctxtag)
    return pure_args_out, pure_out

  return merge_inputs_wrapper  # type: ignore

