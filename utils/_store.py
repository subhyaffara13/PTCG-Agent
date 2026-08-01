
def _store(
    ptr: ir.Value,
    value: ir.Value,
    mask: ir.Value | None = None,
    *,
    cache_modifier: str | None = None,
    eviction_policy: str | None = None,
) -> None:
  if cache_modifier is None:
    cache = tt_dialect.CacheModifier.NONE
  elif cache_modifier != ".ca":
    cache = _STR_TO_CACHE_MODIFIER[cache_modifier]
  else:
    raise ValueError(f"unsupported cache modifier: {cache_modifier}")
  if eviction_policy is None:
    evict = tt_dialect.EvictionPolicy.NORMAL
  else:
    try:
      evict = _STR_TO_EVICTION_POLICY[eviction_policy]
    except KeyError:
      raise ValueError(
          f"unsupported eviction policy: {eviction_policy}"
      ) from None

  if _is_triton_pointer_type(ptr.type):
    ptr_type = tt_dialect.PointerType(ptr.type)
    if isinstance(ptr_type.pointee_type, ir.RankedTensorType):
      raise NotImplementedError("loading from a block pointer is not supported")

  ptr_type = _element_type(ptr.type)
  if not _is_triton_pointer_type(ptr_type):
    raise ValueError(f"unsupported pointer type: {ptr_type}")
  ptr_type = tt_dialect.PointerType(ptr_type)
  if not isinstance(ptr.type, ir.RankedTensorType):
    if isinstance(value.type, ir.RankedTensorType):
      raise ValueError("value cannot be a block if pointer is not a block")
    if mask is not None and isinstance(mask.type, ir.RankedTensorType):
      raise ValueError("mask cannot be a block if pointer is not a block")

  pointee_type = ptr_type.pointee_type
  if isinstance(pointee_type, ir.IntegerType) and pointee_type.width == 1:
    pointee_type = ir.IntegerType.get_signless(8)
    ptr = _ir_cast(
        ptr,
        tt_dialect.PointerType.get(pointee_type, ptr_type.address_space),
        signed=False,
    )

  value = _ir_cast(value, pointee_type, signed=False)
  tt_dialect.store(ptr, value, mask=mask, cache=cache, evict=evict)

