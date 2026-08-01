
def normalize_restrict_and_reload(
    restrict: py_utils.StrOrStrList,
    reload: py_utils.StrOrStrList,
    *,
    restrict_reload: bool = True,
) -> tuple[list[str], list[str]]:
  """Normalize restrict and reload."""
  if isinstance(reload, bool):
    raise ValueError(
        f"reload={reload} is deprecated. Instead use reload='my_module'"
    )

  restrict = py_utils.normalize_str_to_list(restrict)
  reload = py_utils.normalize_str_to_list(reload)

  # Restrict also include the reload
  # This allow to call `adhoc(reload='visu3d')` without explicitly set restrict
  if restrict_reload:
    restrict = _remove_duplicate(restrict + reload)

  if '' in reload:
    raise ValueError(f'reload={reload} contains empty string.')

  return restrict, reload

