
def subs_list(
    subs: Sequence[int | None], src: Sequence[T], base: Sequence[T],
) -> list[T]:
  base_ = iter(base)
  out = [src[i] if i is not None else next(base_) for i in subs]
  sentinel = object()
  assert next(base_, sentinel) is sentinel
  return out

