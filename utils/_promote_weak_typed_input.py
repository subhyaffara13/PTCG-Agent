from typing import Any

def _promote_weak_typed_input(
    in_val:Any, in_aval:AbstractValue, out_aval:AbstractValue
    ) -> tuple[Any, bool]:
  if getattr(in_aval, 'weak_type', False) and not core.typematch(in_aval, out_aval):
    new_dtype = dtypes.result_type(in_val, out_aval)
    return lax.convert_element_type(in_val, new_dtype), True
  else:
    return in_val, False

