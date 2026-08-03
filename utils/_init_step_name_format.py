from typing import Optional

def _init_step_name_format(
    step_name_format: Optional[step_lib.NameFormat[step_lib.Metadata]] = None,
    step_prefix: Optional[str] = None,
    step_format_fixed_length: Optional[int] = None,
):
  return step_name_format or step_lib.standard_name_format(
      step_prefix=step_prefix,
      step_format_fixed_length=step_format_fixed_length,
  )

