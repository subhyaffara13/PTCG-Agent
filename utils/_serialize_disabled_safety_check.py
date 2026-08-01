
def _serialize_disabled_safety_check(
    builder: flatbuffers.Builder, check: _export.DisabledSafetyCheck
) -> int:
  custom_call_target_str = check.is_custom_call()
  custom_call_target = None
  if custom_call_target_str is not None:
    kind = ser_flatbuf.DisabledSafetyCheckKind.custom_call
    custom_call_target = builder.CreateString(custom_call_target_str)
  elif check == _export.DisabledSafetyCheck.platform():
    kind = ser_flatbuf.DisabledSafetyCheckKind.platform
  else:
    raise NotImplementedError(f"serializing DisabledSafetyCheck: {check}")

  ser_flatbuf.DisabledSafetyCheckStart(builder)
  ser_flatbuf.DisabledSafetyCheckAddKind(builder, kind)
  if custom_call_target is not None:
    ser_flatbuf.DisabledSafetyCheckAddCustomCallTarget(
        builder, custom_call_target
    )
  return ser_flatbuf.DisabledSafetyCheckEnd(builder)

