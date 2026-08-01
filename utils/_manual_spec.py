
def _manual_spec(manual_axes, spec: P, mesh) -> P:
  out: list[str | tuple[str | None, ...] | None] = []
  s: str | None | tuple[str, ...]
  for s in spec.partitions:
    if s is None:
      out.append(s)
    elif isinstance(s, tuple):
      temp = [p if p in manual_axes else None for p in s]
      while temp and temp[-1] is None:
        temp.pop()
      if None in temp:
        raise ValueError(f"Invalid spec: {spec}")
      out.append(None if len(temp) == 0 else tuple(temp))
    else:
      out.append(s if s in manual_axes else None)
  _check_unreduced(SpecErrorType.input, mesh, manual_axes, spec)
  return P(*out, unreduced=spec.unreduced, reduced=spec.reduced)

