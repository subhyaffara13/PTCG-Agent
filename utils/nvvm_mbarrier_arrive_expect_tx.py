
def nvvm_mbarrier_arrive_expect_tx(
    barrier: ir.Value,
    expect_tx: ir.Value,
    predicate: ir.Value | None = None,
    scope: nvvm.MemScopeKind | None = None,
):
  # TODO(bchetioui): Remove once jaxlib 0.11.0 is the minimum version.
  first_param, *_ = inspect.signature(nvvm.mbarrier_arrive_expect_tx).parameters.keys()
  if first_param != "addr":
    args = (None, barrier, expect_tx)
  else:
    args = (barrier, expect_tx)
  return nvvm.mbarrier_arrive_expect_tx(
      *args, scope=scope, predicate=predicate  # pyrefly: ignore[bad-argument-type]
  )

