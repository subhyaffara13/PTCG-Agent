
def var_defaults() -> VarDefaults: ...


def var_defaults(
  *, hijax: bool | None = None, ref: bool | None = None
) -> VarDefaultsContext: ...


def var_defaults(
  *, hijax: bool | None = None, ref: bool | None = None
) -> VarDefaultsContext | VarDefaults:
  if hijax is None and ref is None:
    return VarDefaults(
      hijax=VARIABLE_CONTEXT.variable_hijax_stack[-1]
      if VARIABLE_CONTEXT.variable_hijax_stack
      else config.flax_hijax_variable,
      ref=VARIABLE_CONTEXT.variable_ref_stack[-1]
      if VARIABLE_CONTEXT.variable_ref_stack
      else False,
    )

  hijax_prev = None
  if hijax is not None:
    if VARIABLE_CONTEXT.variable_hijax_stack:
      hijax_prev = VARIABLE_CONTEXT.variable_hijax_stack[-1]
      VARIABLE_CONTEXT.variable_hijax_stack[-1] = hijax
    else:
      VARIABLE_CONTEXT.variable_hijax_stack.append(hijax)

  ref_prev = None
  if ref is not None:
    if VARIABLE_CONTEXT.variable_ref_stack:
      ref_prev = VARIABLE_CONTEXT.variable_ref_stack[-1]
      VARIABLE_CONTEXT.variable_ref_stack[-1] = ref
    else:
      VARIABLE_CONTEXT.variable_ref_stack.append(ref)

  return VarDefaultsContext(
    hijax_prev=hijax_prev,
    hijax_new=hijax,
    ref_prev=ref_prev,
    ref_new=ref,
  )

