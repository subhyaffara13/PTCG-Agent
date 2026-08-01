
def _mapped_axis_size(fn, tree, vals, dims, name, axis_size=None):
  if not vals:
    if axis_size is not None:
      return axis_size
    args, kwargs = tree_unflatten(tree, vals)
    raise ValueError(
        f"{name} wrapped function must be passed at least one argument "
        "containing an array or axis_size must be specified, got empty "
        f"*args={args} and **kwargs={kwargs}"
    )

  def _get_axis_size(name: str, x, axis: int) -> core.AxisSize | None:
    shape: tuple[core.AxisSize, ...] = ()
    try:
      shape = np.shape(x)
      return shape[axis]
    except (IndexError, TypeError) as e:
      if not core.valid_jaxtype(x) or not isinstance(axis, int):
        return None  # Suppress the check for custom vmappable types.
      min_rank = axis + 1 if axis >= 0 else -axis
      # TODO(mattjj): better error message here
      raise ValueError(
          f"{name} was requested to map its argument along axis {axis}, "
          f"which implies that its rank should be at least {min_rank}, "
          f"but is only {len(shape)} (its shape is {shape})") from e

  all_mapped_sizes = [
    None if d is None else _get_axis_size(name, x, d)
    for x, d in zip(vals, dims)
  ]
  all_sizes = [s for s in all_mapped_sizes if s is not None]
  if axis_size is not None:
    all_sizes.append(axis_size)
  sizes = core.dedup_referents(all_sizes)
  if len(sizes) == 1:
    sz, = sizes
    return sz
  if not sizes:
    raise ValueError(f"{name} must have at least one non-None value in in_axes "
                     "or axis_size must be specified")

  def _get_argument_type(x):
    try:
      return shaped_abstractify(x).str_short()
    except TypeError: # Catch all for user specified objects that can't be interpreted as a data type
      return "unknown"
  msg = [f"{name} got inconsistent sizes for array axes to be mapped:\n"]
  args, kwargs = tree_unflatten(tree, vals)
  try:
    ba = inspect.signature(fn).bind(*args, **kwargs)
    signature_parameters: list[str] | None = list(ba.signature.parameters.keys())
  except (TypeError, ValueError):
    signature_parameters = None

  def arg_name(key_path):
    if signature_parameters is None:
      return f"args{keystr(key_path)}"
    # args is a tuple, so key_path[0].idx is the index into args.
    i = key_path[0].idx
    # This can happen with star arguments (*args)
    if i >= len(signature_parameters):
      return f"args{keystr(key_path)}"
    res = f"argument {signature_parameters[i]}"
    if len(key_path) > 1:
      res += keystr(key_path[1:])
    return res

  args_paths = [
    f"{arg_name(p)} of type {_get_argument_type(x)}"
    for (p, x) in generate_key_paths(args)
  ]
  kwargs_paths = [
    f"kwargs{keystr(p)} of type {_get_argument_type(x)}"
    for p, x in generate_key_paths(kwargs)
  ]
  key_paths = [*args_paths, *kwargs_paths]
  size_counts = collections.Counter(s for s in all_mapped_sizes if s is not None)
  (sz, ct), *other_counts = counts = size_counts.most_common()

  def _all_sizes_index(sz):
    for i, isz in enumerate(all_mapped_sizes):
      if core.definitely_equal(isz, sz): return i
    assert False, (sz, all_mapped_sizes)

  ex, *examples = (key_paths[_all_sizes_index(sz)] for sz, _ in counts)
  ax, *axs = (dims[_all_sizes_index(sz)] for sz, _ in counts)

  if axis_size is not None:
    msg.append(f"  * the `axis_size` argument was {axis_size};\n")
  if ct == 1:
    msg.append(f"  * one axis had size {sz}: axis {ax} of {ex};\n")
  else:
    msg.append(f"  * most axes ({ct} of them) had size {sz}, e.g. axis {ax} of {ex};\n")
  for ex, ax, (sz, ct) in zip(examples, axs, other_counts):
    if ct == 1:
      msg.append(f"  * one axis had size {sz}: axis {ax} of {ex};\n")
    else:
      msg.append(f"  * some axes ({ct} of them) had size {sz}, e.g. axis {ax} of {ex};\n")
  raise ValueError(''.join(msg)[:-2])  # remove last semicolon and newline


def _mapped_axis_size(args, in_axes):
  """Infer axis size from the first mapped argument.

  shard_map already does a check on all arguments, so just look at first arg.

  Args:
    args: Flat list of arguments.
    in_axes: Flat tuple of axis indices (int or None for each arg).

  Returns:
    The size of the mapped axis.

  Raises:
    ValueError: If no args have a mapped axis.
  """
  if args and in_axes:
    # Fast path: check first arg/axis (most common case).
    if in_axes[0] is not None and hasattr(args[0], "shape"):
      return int(args[0].shape[in_axes[0]])
    # Slow path: scan for first mapped arg.
    if isinstance(in_axes, tuple):
      for arg, ax in zip(args, in_axes):
        if ax is not None and hasattr(arg, "shape"):
          return int(arg.shape[ax])
  raise ValueError("pmap requires at least one argument with a mapped axis.")

