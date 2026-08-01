
def _deserialize_effect(eff: ser_flatbuf.Effect) -> core.Effect:
  effect_type_name = eff.TypeName().decode("utf-8")
  for existing_effect_type in effects.lowerable_effects._effect_types:
    if str(existing_effect_type) == effect_type_name:
      try:
        return existing_effect_type()
      except:
        # TODO: add test
        raise NotImplementedError(
            f"deserializing effect {effect_type_name} that does not have a "
            "nullary class constructor"
        )

  raise NotImplementedError(
      f"cannot deserialize effect type {effect_type_name}"
  )

