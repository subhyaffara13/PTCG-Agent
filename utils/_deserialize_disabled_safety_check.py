
def _deserialize_disabled_safety_check(
    sc: ser_flatbuf.DisabledSafetyCheck,
) -> _export.DisabledSafetyCheck:
  kind = sc.Kind()
  if kind == ser_flatbuf.DisabledSafetyCheckKind.custom_call:
    return _export.DisabledSafetyCheck.custom_call(
        sc.CustomCallTarget().decode("utf-8")
    )
  if kind == ser_flatbuf.DisabledSafetyCheckKind.platform:
    return _export.DisabledSafetyCheck.platform()

  raise ValueError(f"Cannot deserialize DisabledSafetyCheck with unknown kind: {kind}")

