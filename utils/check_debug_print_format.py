
def check_debug_print_format(
    fmt: str, *args: jax_typing.ArrayLike
):
  n_placeholders = 0
  for _, field, spec, conversion in string.Formatter().parse(fmt):
    if field is not None:
      n_placeholders += 1
    if spec or conversion:
      raise ValueError(
          "The format string should not contain any format specs or conversions"
      )
    if field:
      raise ValueError(
          "The format string should not reference arguments by position or name"
      )

  if len(args) != n_placeholders:
    raise TypeError(
        f"The format string expects {n_placeholders} "
        f"argument{'' if n_placeholders == 1 else 's'}, but got {len(args)}"
    )

