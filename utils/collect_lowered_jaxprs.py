
def collect_lowered_jaxprs() -> Generator[
    Sequence[tuple[core.ClosedJaxpr, mlir.ir.Module]],
    None,
    None,
]:
  """
  Collects all the pairs of (jaxpr, mlir_module) that are lowered.
  """
  assert thread_local_state.collect_lowered_jaxprs is None
  collection: list[tuple[core.ClosedJaxpr, mlir.ir.Module]] = []
  thread_local_state.collect_lowered_jaxprs = collection
  try:
    yield collection
  finally:
    thread_local_state.collect_lowered_jaxprs = None

