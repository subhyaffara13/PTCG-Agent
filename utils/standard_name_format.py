from typing import Optional

def standard_name_format(
    *,
    step_prefix: Optional[str] = None,
    step_format_fixed_length: Optional[int] = None,
    single_host_load_and_broadcast: bool = False,
) -> NameFormat[Metadata]:
  """Returns NameFormat for 'standard' steps for common Orbax use cases.

  NOTE: Ignores uncommitted checkpoints.

  Naming examples:
   * step_prefix=None    step_format_fixed_length=None  ->  23
   * step_prefix=None    step_format_fixed_length=4     ->  0023
   * step_prefix=step    step_format_fixed_length=None  ->  step_23
   * step_prefix=step    step_format_fixed_length=4     ->  step_0023

  Args:
    step_prefix: Optional fixed string prefixed to step. Note an *underscore* is
      appended before applying it.
    step_format_fixed_length: Optional length of the zero padded step. e.g. 6
      for 000123.
    single_host_load_and_broadcast: If True, the jax process=0 will list all
      steps and broadcast them to all other processes. NOTE: Ignored if jax
      backend is not multi controller.
  """
  return _StandardNameFormat(
      step_prefix=step_prefix,
      step_format_fixed_length=step_format_fixed_length,
      single_host_load_and_broadcast=single_host_load_and_broadcast,
  )


def standard_name_format(
    *,
    step_prefix: str | None = None,
    step_format_fixed_length: int | None = None,
    single_host_load_and_broadcast: bool = False,
) -> NameFormat[CheckpointMetadata[None]]:
  """Returns NameFormat for 'standard' steps for common Orbax use cases.

  NOTE: Ignores uncommitted checkpoints.

  Naming examples:
   * step_prefix=None    step_format_fixed_length=None  ->  23
   * step_prefix=None    step_format_fixed_length=4     ->  0023
   * step_prefix=step    step_format_fixed_length=None  ->  step_23
   * step_prefix=step    step_format_fixed_length=4     ->  step_0023

  Args:
    step_prefix: Optional fixed string prefixed to step. Note an *underscore* is
      appended before applying it.
    step_format_fixed_length: Optional length of the zero padded step. e.g. 6
      for 000123.
    single_host_load_and_broadcast: If True, the jax process=0 will list all
      steps and broadcast them to all other processes. NOTE: Ignored if jax
      backend is not multi controller.
  """
  return _StandardNameFormat(
      step_prefix=step_prefix,
      step_format_fixed_length=step_format_fixed_length,
      single_host_load_and_broadcast=single_host_load_and_broadcast,
  )

