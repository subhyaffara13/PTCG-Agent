
def _set_up_aliases(input_output_aliases, avals_in, avals_out,
                    donated_args, arg_memory_kinds, result_memory_kinds,
                    in_layouts, out_layouts, result_shardings):
  if input_output_aliases is None:
    input_output_aliases: list[int | None] = [None] * len(avals_in)
  else:
    input_output_aliases = list(input_output_aliases)
  # To match-up in-avals to out-avals we only care about the number of
  # bytes, so we strip off unrelated aval metadata (eg. the named shape)
  strip_metadata = lambda a: (a if a is core.abstract_token else
                              core.ShapedArray(a.shape, a.dtype))
  avals_in = map(strip_metadata, avals_in)
  avals_out = map(strip_metadata, avals_out)

  # Both arg and result memory kinds need to be specified to donate based on
  # the memory kind. For jit's where out_shardings is not specified, we don't
  # know the memory kind so don't condition the logic based on the memory kind.
  # TODO(yashkatariya): Note that this logic should be in C++ where we make
  # donation decisions are made after SPMD propagation passes and memory
  # placement passes so that we have all the information.
  if (arg_memory_kinds is None or result_memory_kinds is None or
      any(a is None for a in arg_memory_kinds) or
      any(r is None for r in result_memory_kinds)):
    arg_memory_kinds = [None] * len(avals_in)
    result_memory_kinds = [None] * len(avals_out)

  donations = collections.defaultdict(collections.deque)
  for i, (aval, am, donated, aliased) in enumerate(
      zip(avals_in, arg_memory_kinds, donated_args, input_output_aliases)):
    if donated and aliased is None:
      donations[(aval, am)].append(i)

  xla_donated_args = None
  out_donated_args = list(donated_args)
  in_out_layout_not_none = in_layouts is not None and out_layouts is not None
  for i, (aval, rm) in enumerate(zip(avals_out, result_memory_kinds)):
    # Only donate if memory kinds match. Relax this when the compiler can
    # donate across memories.
    key = (aval, rm)
    if donations.get(key, ()):
      input_id = donations[key].popleft()
      out_donated_args[input_id] = False
      if (in_out_layout_not_none and
          isinstance(in_layouts[input_id], AutoLayoutSingleton) and
          not isinstance(out_layouts[i], AutoLayoutSingleton)):
        raise ValueError(
            f"Input layout being donated was {in_layouts[input_id]} while"
            f" output layout was {out_layouts[i]}. Did you mean to set the"
            " **output layout** to **Layout.AUTO**?\nThis will"
            " allow for the input and output layout to be chosen by XLA and"
            " not the layout of the output which might not be optimal.")
      if (in_out_layout_not_none and
          not isinstance(in_layouts[input_id], AutoLayoutSingleton) and
          isinstance(out_layouts[i], AutoLayoutSingleton)):
        raise ValueError(
            f"Input layout being donated was {in_layouts[input_id]} while"
            f" output layout was {out_layouts[i]}. Did you mean to set the"
            " **input layout** to **Layout.AUTO**?\nThis will allow"
            " for the input and output layout to be chosen by XLA and not the"
            " layout of the input which might not be optimal.")
      if (in_layouts is None or out_layouts is None or
          in_layouts[input_id] == out_layouts[i]) and (
              result_shardings is None or not (
              (s := result_shardings[i]) is None or contains_unconstrained(s))):
        input_output_aliases[input_id] = i
      else:
        # Fallback to xla donation if layouts don't match.
        if xla_donated_args is None:
          xla_donated_args = [False] * len(avals_in)
        xla_donated_args[input_id] = True

  aliased_output_ids = {i for i in input_output_aliases if i is not None}

  results_not_matched = collections.defaultdict(collections.deque)
  for i, (aval, rm) in enumerate(zip(avals_out, result_memory_kinds)):
    if i not in aliased_output_ids and aval is not core.abstract_token:
      results_not_matched[(aval.size, rm)].append(i)  # pyrefly: ignore[missing-attribute]

  # For each donated argument that hasn't been aliased or donated to XLA, try to
  # find an output array with matching size ignoring shapes. If a matching
  # output array is found, then the argument is donated to XLA.
  # Similar to the aliasing logic above, an argument is donated to XLA even if
  # its layout and the output's layout don't match. This is being done to
  # provide more opportunities for XLA to reuse the donated arguments.
  for input_idx in range(len(out_donated_args)):
    # If the argument is not a token and hasn't been aliased or donated to XLA,
    # then try to find an output array with matching size.
    if (out_donated_args[input_idx]
        and avals_in[input_idx] is not core.abstract_token):
      key = (
          # pyrefly: ignore[missing-attribute]
          avals_in[input_idx].size,
          arg_memory_kinds[input_idx],
      )
      if results_not_matched.get(key, ()):
        # XLA donate the argument because there's a matching output array.
        results_not_matched[key].popleft()
        out_donated_args[input_idx] = False
        if xla_donated_args is None:
          xla_donated_args = [False] * len(avals_in)
        xla_donated_args[input_idx] = True

  return input_output_aliases, out_donated_args, xla_donated_args

