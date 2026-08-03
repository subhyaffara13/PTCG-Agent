import functools

def emit_pipeline_with_allocations(
    body,
    *,
    grid,
    in_specs=(),
    out_specs=(),
):
  """Creates pallas pipeline and top-level allocation preparation functions.

  Args:
    body: pallas kernel to set up pipeline for.
    grid: a pallas grid definition.
    in_specs: input pallas block specs
    out_specs: output pallas block specs

  Returns:
    (emit_pipeline, make_allocations) function pair, where
      - emit_pipeline is the pallas pipeline function.
      - make_allocations is a function to create buffered refs for the inner
        pipeline that can be created at the top-level of a pallas call to be
        reused across multiple invocations of the inner pipeline.
  """
  make_allocations = functools.partial(_make_pipeline_allocations,
                    in_specs=in_specs,
                    out_specs=out_specs,
                    grid=grid)
  pipeline = emit_pipeline(
      body,
      grid=grid,
      in_specs=in_specs,
      out_specs=out_specs)
  return pipeline, make_allocations

