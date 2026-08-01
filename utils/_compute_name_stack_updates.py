
def _compute_name_stack_updates(
    old_name_stack: list[str],
    new_name_stack: list[str]
) -> tuple[list[str], list[str]]:
  """Computes the popped/pushed items to the name stack after an update.

  Args:
    old_name_stack: The name stack prior to the update.
    new_name_stack: The name stack after the update.

  Returns:
    popped: A list of names popped from the name stack as part of the update.
    pushed: A list of names pushed to the name stack as part of the update.
  """
  common_prefix_idx = 0
  for i, (old, new) in enumerate(unsafe_zip(old_name_stack, new_name_stack)):
    if old == new:
      common_prefix_idx = i+1
    else:
      break
  return old_name_stack[common_prefix_idx:], new_name_stack[common_prefix_idx:]


def _compute_name_stack_updates(
    old_name_stack: list[str],
    new_name_stack: list[str]
) -> tuple[list[str], list[str]]:
  common_prefix_idx = 0
  for i, (old, new) in enumerate(unsafe_zip(old_name_stack, new_name_stack)):
    if old == new:
      common_prefix_idx = i+1
    else:
      break
  return old_name_stack[common_prefix_idx:], new_name_stack[common_prefix_idx:]

