from typing import Any

def shard_args(
    shardings: Sequence[JSharding],
    layouts: Sequence[Any | None],
    copy_semantics: Sequence[xc.ArrayCopySemantics],
    args: Sequence[Any],
    canonicalize: bool = True,
) -> Sequence[xc.ArrayImpl]:
  # Fast path for one argument.
  if len(args) == 1:
    arg = args[0]
    if canonicalize:
      arg = dtypes.canonicalize_value(arg)
    handler = shard_arg_handlers.get(type(arg), None)
    if handler is None:
      raise dtypes.InvalidInputException(
          f"Argument of type {type(arg)} is not a valid JAX type.")
    return handler([arg], shardings, layouts, copy_semantics)

  # type(arg) -> (list[indices], list[args], list[shardings], list[layouts],
  #               list[copy_semantics])
  batches = collections.defaultdict(lambda: ([], [], [], [], []))
  for i, (arg, sharding, layout, cs) in enumerate(
      safe_zip(args, shardings, layouts, copy_semantics)):
    if canonicalize:
      arg = dtypes.canonicalize_value(arg)
    batch = batches[type(arg)]
    batch[0].append(i)
    batch[1].append(arg)
    batch[2].append(sharding)
    batch[3].append(layout)
    batch[4].append(cs)

  # Call `shard_arg_handlers` per batch and build a flat list of arrays returned
  # from each call in the same order as `args`. Since `batches` is grouped by
  # types, we cannot simply flatten the results and we have to use the original
  # indices to put each array back to its original position.
  results: list[typing.Array | None] = [None] * len(args)
  for t, (indices, a, s, l, xcs) in batches.items():
    handler = shard_arg_handlers.get(t, None)
    if handler is None:
      raise dtypes.InvalidInputException(
          f"Argument of type {t} is not a valid JAX type.")
    outs = handler(a, s, l, xcs)
    for i, out in safe_zip(indices, outs):
      results[i] = out
  assert all(result is not None for result in results)
  return results

