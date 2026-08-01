
def _check_carry_type(name, body_fun, in_carry, out_carry):
  try:
    sig = inspect.signature(body_fun)
  except (ValueError, TypeError):
    sig = None
  carry_name = sig and list(sig.parameters)[0]
  if carry_name:
    component = lambda p: (f'the input carry component {carry_name}{keystr(p)}'
                           if p else f'the input carry {carry_name}')
  else:
    component = lambda p: (f'the input carry at path {keystr(p)}'
                           if p else 'the input carry')
  if in_carry.tree != out_carry.tree:
    try:
      out_carry_unflat = out_carry.unflatten()
    except:
      out_carry_unflat = None

    if out_carry_unflat is None:
      differences = (f'the input tree structure is:\n{in_carry.tree}\n' +
                     f'the output tree structure is:\n{out_carry.tree}\n')
    else:
      diffs = [f'{component(path)} is a {thing1} but the corresponding component '
               f'of the carry output is a {thing2}, so {explanation}'
               for path, thing1, thing2, explanation
               in equality_errors(in_carry.unflatten(), out_carry.unflatten())]
      if len(diffs) == 0:
        return  # the trees may have different aux data, but structures are same
      elif len(diffs) == 1:
        differences = f'{_capitalize(diffs[0])}.\n'
      else:
        differences = ('\n'.join(f'  * {d};\n' for d in diffs[:-1])
                       + f'  * {diffs[-1]}.\n')
    raise TypeError(
        f"{name} function carry input and carry output must have the same "
        "pytree structure, but they differ:\n\n"
        f"{differences}\n"
        "Revise the function so that the carry output has the same pytree "
        "structure as the carry input.")
  if not all(_map(core.typematch, in_carry, out_carry)):
    diffs = [f'{component(path)} has type {in_aval.str_short()}'
             ' but the corresponding output carry component has type '
             f'{out_aval.str_short()}'
             f'{core.aval_mismatch_extra(in_aval, out_aval)}'
             for path, in_aval, out_aval in zip(in_carry.paths, in_carry, out_carry)
             if not core.typematch(in_aval, out_aval)]

    if len(diffs) == 0:
      return  # seems unreachable but in any case we don't have a good error msg
    if len(diffs) == 1:
      differences = f'{_capitalize(diffs[0])}.\n'
    else:
      differences = ('\n'.join(f'  * {d};\n' for d in diffs[:-1])
                     + f'  * {diffs[-1]}.\n')

    # TODO(rdyro): extend this to also cover reduced and unreduced.
    pvary_applications = [
        f'applying `jax.lax.pcast(..., '
        f"{tuple(out_aval.mat.varying - in_aval.mat.varying)}, to='varying')`, "
        f'to the initial carry value corresponding to {component(path)}'
        for path, in_aval, out_aval in zip(in_carry.paths, in_carry, out_carry)
        if not core.typematch(in_aval, out_aval) and
        isinstance(in_aval, ShapedArray) and isinstance(out_aval, ShapedArray)
        and in_aval.mat.varying != out_aval.mat.varying
        and out_aval.mat.varying - in_aval.mat.varying]

    if not pvary_applications:
      pvary_msg = ''
    elif len(pvary_applications) == 1:
      pvary_msg = f'This might be fixed by {pvary_applications[0]}.\n'
    else:
      pvary_msg = ('This might be fixed by:\n' +
                   '\n'.join(f'  * {d};\n' for d in pvary_applications[:-1])
                   + f'  * {pvary_applications[-1]}.\n')
    if pvary_msg:
      pvary_msg += ("See https://docs.jax.dev/en/latest/notebooks/shard_map.html#scan-vma "
                    "for more information.\n\n")

    raise TypeError(
        f"{name} function carry input and carry output must have equal types, "
        "but they differ:\n\n"
        f"{differences}\n"
        f"{pvary_msg}"
        "Revise the function so that all output types match the corresponding "
        "input types.")

