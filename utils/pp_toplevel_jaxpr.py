
def pp_toplevel_jaxpr(jaxpr_to_print: Jaxpr, *,
                      source_info: bool = False,
                      print_shapes: bool = True,
                      custom_pp_eqn_rules : bool = True,
                      name_stack: bool = False,
                      print_effects: bool = False) -> pp.Doc:
    context = JaxprPpContext(_dropvars(jaxpr_to_print))
    settings = JaxprPpSettings(
        source_info=source_info,
        print_shapes=print_shapes,
        custom_pp_eqn_rules=custom_pp_eqn_rules,
        name_stack=name_stack,
        print_effects=print_effects)

    # Compute how many times each jaxpr is used.
    names = defaultdict[Jaxpr, str](lambda: "jaxpr")
    jaxpr_counts = Counter[Jaxpr]()
    s = deque([jaxpr_to_print])
    while s:
      jaxpr = s.popleft()
      jaxpr_counts[jaxpr] += 1
      if jaxpr is not jaxpr_to_print and len(jaxpr.eqns) > 10:
        jaxpr_counts[jaxpr] += 1
      for eqn in jaxpr.eqns:
        # TODO(slebedev): Come up with a more elaborate heuristic for name=.
        name = eqn.params.get("name")
        if name is None:
          s.extend(jaxprs_in_params(eqn.params))
          continue
        name = name.strip("<>")  # <lambda> -> lambda
        for subjaxpr in jaxprs_in_params(eqn.params):
          s.append(subjaxpr)
          names.setdefault(subjaxpr, name)

    # Pull jaxprs occurring more than once to the top-level, making sure
    # that their names are unique.
    name_counts = Counter[str]()
    shared = []
    for jaxpr, c in jaxpr_counts.items():
      if c == 1:
        continue
      name = names[jaxpr]
      if (count := name_counts[name]) > 0:
        name_counts[name] += 1
        name += str(count)
        name_counts[name] += 1
      else:
        name_counts[name] += 1
      context.shared_jaxpr_names.add(name)
      context.shared_jaxprs[jaxpr] = name
      shared.append((name, jaxpr))

    docs = []
    for name, jaxpr in shared:
      docs.append(pp_shared_jaxpr(name, jaxpr, context, settings))
    docs.append(pp_jaxpr(jaxpr_to_print, context, settings))
    return pp.concat(docs)

