
def subs_list2(
    subs1: Sequence[int | None], subs2: Sequence[int | None],
    src1: Sequence[T], src2: Sequence[T], base: Sequence[T],
) -> list[T]:
  assert len(subs1) == len(subs2)
  base_ = iter(base)
  out = [src1[f1] if f1 is not None else src2[f2] if f2 is not None else
         next(base_) for f1, f2, in zip(subs1, subs2)]
  sentinel = object()
  assert next(base_, sentinel) is sentinel
  return out

