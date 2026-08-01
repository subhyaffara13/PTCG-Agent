
def _resolve_side_effect_type(
    has_side_effects: bool | tpu_core.SideEffectType,
) -> bool | tpu_custom_call.TpuSideEffectType:
  match has_side_effects:
    case bool():
      return has_side_effects
    case tpu_core.SideEffectType.PURE:
      return tpu_custom_call.TpuSideEffectType.PURE
    case tpu_core.SideEffectType.DATAFLOW_SIDE_EFFECTING:
      return tpu_custom_call.TpuSideEffectType.DATAFLOW_SIDE_EFFECTING
    case tpu_core.SideEffectType.SIDE_EFFECTING:
      return tpu_custom_call.TpuSideEffectType.SIDE_EFFECTING
    case _:
      raise ValueError(f"Invalid side effect type: {has_side_effects}")

