
def _make_pipeline_allocations(
    *refs,
    in_specs=(),
    out_specs=(),
    tiling: Tiling | None = None,
    grid=(),
):
  """Create BufferedRefs for the pipeline.

  This function creates buffered refs for an inner pipeline that can be
  created at the top-level of a pallas call such that they may be reused across
  multiple invocations of the inner pipeline.

  Args:
    in_specs: input pallas block specs
    out_specs: output pallas block specs
    grid: grid to use for the pipeline.

  Returns:
    A list of BufferedRefs, one corresponding to each ref specified in the
    in_specs and out_specs.
  """
  # TODO(levskaya): generalize argument tree handling here and in emit_pipeline.
  num_in_specs = len(in_specs)
  in_specs = _normalize_specs(in_specs)
  out_specs = _normalize_specs(out_specs)
  in_refs = refs[:num_in_specs]
  out_refs = refs[num_in_specs:]
  def make_input_bref(in_spec, in_ref):
    in_aval = _ref_to_value_aval(in_ref)
    buffer_count = 2
    use_lookahead = False
    if has_buffering := in_spec.pipeline_mode is not None:
      buffer_count = in_spec.pipeline_mode.buffer_count
      use_lookahead = in_spec.pipeline_mode.use_lookahead
    if use_lookahead and grid is None:
      raise ValueError("Grid must be specified when using lookahead.")
    is_trivial = _spec_has_trivial_windowing(in_spec, grid, in_aval.shape)
    if not has_buffering and is_trivial:
      buffer_count = 1

    return BufferedRef.input(
        in_spec,
        in_aval,
        buffer_count,
        grid_rank=len(grid),
        use_lookahead=use_lookahead,
        source_memory_space=in_ref.memory_space,
        tiling=tiling,
        is_trivial_windowing=is_trivial,
    )
  in_brefs = jax.tree.map(make_input_bref, in_specs, in_refs)
  def make_output_bref(out_spec, out_ref):
    out_aval = _ref_to_value_aval(out_ref)
    buffer_count = 2
    if has_buffering := out_spec.pipeline_mode is not None:
      buffer_count = out_spec.pipeline_mode.buffer_count
      if out_spec.pipeline_mode.use_lookahead:
        raise ValueError("Output buffering does not support lookahead.")
    is_trivial = _spec_has_trivial_windowing(out_spec, grid, out_aval.shape)
    if not has_buffering and is_trivial:
      buffer_count = 1

    return BufferedRef.output(
        out_spec,
        out_aval,
        buffer_count,
        source_memory_space=out_ref.memory_space,
        tiling=tiling,
        is_trivial_windowing=is_trivial,
    )
  out_brefs = jax.tree.map(make_output_bref, out_specs, out_refs)
  return (*in_brefs, *out_brefs)

