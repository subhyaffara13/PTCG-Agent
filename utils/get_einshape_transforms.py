
def get_einshape_transforms(
    equation: str,
    input_shape: tuple[int, ...],
    **sizes: int,
) -> list[Transform]:
  """Parses an einshape equation into a sequence of transforms.

  Args:
    equation: String of the form "ab(cd)->cabd".
    input_shape: The shape of the input array.
    **sizes: Integer sizes for dimensions that are split and cannot be inferred.

  Returns:
    A list of Split, Transpose, and Merge transforms.
  """
  lhs, rhs = _parse_equation(equation)

  # Validate LHS against input shape
  if len(lhs) != len(input_shape):
    raise ValueError(
        f"Equation LHS has {len(lhs)} groups but input has {len(input_shape)}"
        f" dims. LHS: {lhs}, Input shape: {input_shape}"
    )

  dim_sizes: dict[str, int] = {}

  # Populate known sizes from input
  for i, group in enumerate(lhs):
    shape_val = input_shape[i]
    if len(group) == 1:
      name = group[0]
      if name in dim_sizes and dim_sizes[name] != shape_val:
        raise ValueError(
            f"Inconsistent size for {name}: {dim_sizes[name]} vs {shape_val}"
        )
      dim_sizes[name] = shape_val
    else:
      # We have a merged dimension on LHS, need to split
      known_product = 1
      unknown_dims = []
      for name in group:
        if name in sizes:
          dim_sizes[name] = sizes[name]
          known_product *= sizes[name]
        elif name in dim_sizes:
          known_product *= dim_sizes[name]
        else:
          unknown_dims.append(name)

      if not unknown_dims:
        if known_product != shape_val:
          raise ValueError(
              f"Size mismatch for group {group}: expected {shape_val}, got"
              f" {known_product}"
          )
      elif len(unknown_dims) == 1:
        if shape_val % known_product != 0:
          raise ValueError(
              f"Cannot split size {shape_val} with known sizes {known_product}"
          )
        inferred_size = shape_val // known_product
        dim_sizes[unknown_dims[0]] = inferred_size
      else:
        raise ValueError(
            f"Ambiguous split for {group} with size {shape_val}. Unknowns:"
            f" {unknown_dims}. Provide sizes via kwargs."
        )

  # Check if all RHS dims are known
  flat_rhs = [name for group in rhs for name in group]
  for name in flat_rhs:
    if name not in dim_sizes:
      if name in sizes:
        dim_sizes[name] = sizes[name]
      else:
        raise ValueError(f"Unknown dimension {name} in RHS")

  ops: list[Transform] = []

  # 1. Decompose LHS
  current_idx = 0
  for group in lhs:
    if len(group) > 1:
      atomic_sizes = tuple(dim_sizes[name] for name in group)
      ops.append(SplitDims(current_idx, atomic_sizes))
      current_idx += len(group)
    else:
      current_idx += 1

  # 2. Transpose
  lhs_atomic_order = [name for group in lhs for name in group]
  rhs_atomic_order = [name for group in rhs for name in group]

  if set(lhs_atomic_order) != set(rhs_atomic_order):
    raise NotImplementedError(
        "Only reordering/splitting/merging supported (no broadcast yet)."
    )

  if lhs_atomic_order != rhs_atomic_order:
    perm = tuple(lhs_atomic_order.index(name) for name in rhs_atomic_order)
    ops.append(Transpose(perm))

  # 3. Compose RHS
  current_idx = 0
  for group in rhs:
    if len(group) > 1:
      ops.append(MergeDims(current_idx, len(group)))
      current_idx += 1
    else:
      current_idx += 1
  return ops

