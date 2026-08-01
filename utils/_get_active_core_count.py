
def _get_active_core_count(module: ir.Module) -> int | None:

  def get_core_parallel_dim_size(
      dim_semantics: ir.ArrayAttr,
      iter_bounds: ir.DenseI64ArrayAttr,
      other_subkernel_core_dim_size: int | None = None) -> int | None:

    if len(iter_bounds) != len(dim_semantics):
      raise ValueError(
          "The iteration bounds and dimension semantics attributes must have"
          " the same number of elements."
      )

    subkernel_core_dim_size = None

    for dim_idx, (dim_size, dim_sem) in enumerate(
        zip(iter_bounds, dim_semantics)
    ):
      if str(dim_sem) != "#tpu.dimension_semantics<core_parallel>":
        continue

      if ir.ShapedType.is_dynamic_size(dim_size):
        raise ValueError(
            "The iteration bound corresponding to the core-parallel dimension "
            f"{dim_idx} must be statically known."
        )
      if subkernel_core_dim_size is not None:
        raise ValueError(
            "A single Mosaic subkernel cannot contain multiple core sharding "
            "dimensions."
        )
      if (
          other_subkernel_core_dim_size is not None
          and other_subkernel_core_dim_size != dim_size
      ):
        raise ValueError(
            "The iteration bound corresponding to the core-parallel dimension "
            "be the same across all subkernels."
        )
      subkernel_core_dim_size = dim_size

    return subkernel_core_dim_size

  core_parallel_dim_size = None

  for op in module.body.operations:
    if op.operation.name != "func.func":
      continue

    if (
        "iteration_bounds" not in op.attributes
        or "dimension_semantics" not in op.attributes
    ):
      continue

    try:
      iter_bounds = ir.DenseI64ArrayAttr(op.attributes["iteration_bounds"])
    except ValueError as e:
      e.add_note("The iteration bounds attribute must be an array.")
      raise
    try:
      dim_semantics = ir.ArrayAttr(op.attributes["dimension_semantics"])
    except ValueError as e:
      e.add_note("The dimension semantics attribute must be an array.")
      raise

    core_parallel_dim_size = get_core_parallel_dim_size(
        dim_semantics=dim_semantics,
        iter_bounds=iter_bounds,
        other_subkernel_core_dim_size=core_parallel_dim_size,
    )

  return core_parallel_dim_size

