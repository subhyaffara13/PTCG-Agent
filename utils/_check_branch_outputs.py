
def _check_branch_outputs(
    api_name, name1, name2, f1, f2, out_avals1, out_avals2) -> None:
  info1 = api_util.fun_sourceinfo(f1)
  info2 = api_util.fun_sourceinfo(f2)
  try:
    outs1 = out_avals1.unflatten()
  except:
    paths = [None] * len(out_avals1)
    component = lambda _: ''
  else:
    leaves_and_paths, _ = tree_flatten_with_path(outs1)
    paths, _ = unzip2(leaves_and_paths)
    component = lambda p: f' at path {keystr(p)}' if p else ''

  if out_avals1.tree != out_avals2.tree:
    diffs = [f'{name1} output{component(p)} is a {thing1} but '
             f'{name2} output{component(p)} is a {thing2}, so {expl}'
             for p, thing1, thing2, expl
             in equality_errors_pytreedef(out_avals1.tree, out_avals2.tree)]

    if len(diffs) == 0:
      return  # the trees may have different aux data, but structures are same
    elif len(diffs) == 1:
      differences = f'{diffs[0]}.\n'
    else:
      differences = ('\n'.join(f'  * {d};\n' for d in diffs[:-1])
                     + f'  * {diffs[-1]}.\n')

    raise TypeError(
        f'{api_name} branch outputs must have the same pytree structure, but '
        'they differ:\n\n'
        f'{name1} is {info1}\n' + f'{name2} is {info2}\n\n'
        f'{differences}\n'
        f'Revise {name1} and/or {name2} so that they have the same pytree '
        'structure.')

  if not all(map(core.typematch, out_avals1, out_avals2)):
    diffs = [f'the output of {name1}{component(p)} has type {a1.str_short()}'
             f' but the corresponding output of {name2} has type '
             f'{a2.str_short()}{core.aval_mismatch_extra(a1, a2)}'
             for p, a1, a2 in zip(paths, out_avals1, out_avals2)
             if not core.typematch(a1, a2)]
    if len(diffs) == 0:
      return  # seems unreachable but in any case we don't have a good error msg
    elif len(diffs) == 1:
      differences = f'{_capitalize(diffs[0])}.\n'
    else:
      differences = ('\n'.join(f'  * {d};' for d in diffs[:-1])
                     + f'\n  * {diffs[-1]}.\n')

    # TODO(rdyro): extend this to also cover reduced and unreduced.
    pvary_applications = [
        f"applying `jax.lax.pcast(..., "
        f"{tuple(a1.mat.varying - a2.mat.varying)}, to='varying')` to the"
        f" output of {n}{component(p)}"
        for p, aval1, aval2 in zip(paths, out_avals1, out_avals2)
        for n, a1, a2 in [(name1, aval2, aval1), (name2, aval1, aval2)]
        if not core.typematch(a1, a2) and
        isinstance(a1, core.ShapedArray) and isinstance(a2, core.ShapedArray)
        and a1.mat.varying != a2.mat.varying
        and a2.mat.varying - a1.mat.varying]

    if not pvary_applications:
      pvary_msg = ''
    elif len(pvary_applications) == 1:
      pvary_msg = f'This might be fixed by {pvary_applications[0]}.\n'
    else:
      pvary_msg = ('This might be fixed by:\n' +
                   '\n'.join(f'  * {d};' for d in pvary_applications[:-1])
                   + f'\n  * {pvary_applications[-1]}.\n')
    if pvary_msg:
      pvary_msg += ("See https://docs.jax.dev/en/latest/notebooks/shard_map.html#scan-vma "
                    "for more information.\n\n")

    raise TypeError(
        f'{api_name} branches must have equal output types but they differ.\n\n'
        f'{name1} is {info1}\n' + f'{name2} is {info2}\n\n'
        f'{differences}\n'
        f'{pvary_msg}'
        f'Revise {name1} and/or {name2} so that all output types match.')

