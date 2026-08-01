
def _make_range(start: int, end: int) -> ir.Value:
  if end <= start:
    raise ValueError(
        f"end must be greater than start, but got: {end} <= {start}"
    )
  if max(start, end) >= 2**32:
    raise ValueError("start and end must fit in int32")
  return tt_dialect.make_range(
      ir.RankedTensorType.get([end - start], ir.IntegerType.get_signless(32)),
      start,
      end,
  )

