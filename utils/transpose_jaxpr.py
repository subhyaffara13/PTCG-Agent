
def transpose_jaxpr(jaxpr: core.ClosedJaxpr, in_linear: bool | Sequence[bool],
                    out_zeros: bool | Sequence[bool],
                    ) -> tuple[core.ClosedJaxpr, list[bool]]:
  if isinstance(in_linear, bool):
    in_linear = (in_linear,) * len(jaxpr.in_avals)
  if isinstance(out_zeros, bool):
    out_zeros = (out_zeros,) * len(jaxpr.out_avals)
  return _transpose_jaxpr(jaxpr, tuple(in_linear), tuple(out_zeros))

