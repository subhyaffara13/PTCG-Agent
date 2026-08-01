
def _serialize_effect(builder: flatbuffers.Builder, eff: core.Effect) -> int:
  try:
    eff_replica = eff.__class__()
  except Exception:
    raise NotImplementedError(
        f"Effect {eff} must have a nullary constructor to be serializable"
    )
  try:
    hash_eff = hash(eff)
    hash_eff_replica = hash(eff_replica)
  except Exception:
    raise NotImplementedError(
        f"Effect {eff} must be hashable to be serializable"
    )
  if eff != eff_replica or hash_eff != hash_eff_replica:
    raise NotImplementedError(
      f"Effect {eff} must have a nullary class constructor that produces an "
      "equal effect object."
    )
  effect_type_name = str(eff.__class__)
  effect_type_name_offset = builder.CreateString(effect_type_name)
  ser_flatbuf.EffectStart(builder)
  ser_flatbuf.EffectAddTypeName(builder, effect_type_name_offset)
  return ser_flatbuf.ExportedEnd(builder)

