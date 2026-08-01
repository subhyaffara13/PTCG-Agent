
def check_array_xla_sharding_layout_match(
    args,
    in_shardings: Sequence[JSharding],
    in_layouts: Sequence[Layout],
    arg_names: Sequence[str]
) -> None:
  errors = []
  num_errors = 5
  for arg, xs, xl, name in zip(args, in_shardings, in_layouts, arg_names):
    if not isinstance(arg, array.ArrayImpl):
      continue
    if isinstance(xs, UnspecifiedValue):
      continue

    db_xs = check_device_backend_on_shardings([xs])

    if (not db_xs and arg._committed and
        not arg.sharding.is_equivalent_to(xs, arg.ndim)):
      errors.append((
          f"Argument {name} with shape {arg.aval.str_short()}:\n"
          f"  Passed sharding: {arg.sharding}\n"
          f"  Required sharding: {xs}",
          "sharding"))

    if (not db_xs and arg._committed and
        arg.format.layout is not None and xl is not None and
        arg.format.layout != xl):
      errors.append((
          f"Argument {name} with shape {arg.aval.str_short()}:\n"
          f"  Passed layout: {arg.format.layout}\n"
          f"  Required layout: {xl}",
          "layout"))

  if errors:
    first_errors, error_kinds = unzip2(errors[:num_errors])
    str_errors = '\n'.join(first_errors)
    if all(k == 'sharding' for k in error_kinds):
      kind_str = r'shardings'
    elif all(k == 'layout' for k in error_kinds):
      kind_str = 'layouts'
    else:
      kind_str = 'shardings and layouts'
    num_mismatch_str = (
        f"the {len(errors)} mismatches" if len(errors) < num_errors else
        f"{num_errors} mismatches out of {len(errors)}")
    raise ValueError(
        f"Computation was compiled for input {kind_str} that disagree with the "
        f"{kind_str} of arguments passed to it. "
        f"Here are {num_mismatch_str}:\n{str_errors}")

