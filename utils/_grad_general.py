
def _grad_general(
    f: tp.Callable[..., tp.Any],
    argnums: int | DiffState | tp.Sequence[int | DiffState],
    has_aux: bool,
    holomorphic: bool,
    allow_int: bool,
    return_value: bool,
    graph: bool,
    graph_updates: bool,
) -> tp.Callable[..., tp.Any]:

  transform = jax.value_and_grad if return_value else jax.grad

  extract.check_prefix(argnums, 'argnums', 'grad', graph, graph_updates)

  if not graph or not graph_updates:

    gradded_fn = transform(
        SimpleGradFn(f, has_aux, graph=graph),
        argnums=argnums,  # type: ignore[arg-type]
        has_aux=True,
        holomorphic=holomorphic,
        allow_int=allow_int,
    )

    def tree_grad_wrapper(*args, **kwargs):
      if graph:
        diff_argnums = (argnums,) if isinstance(argnums, int) else argnums
        args_prefix = tuple(
          i in diff_argnums for i in range(len(args))
        )
        args, kwargs = extract.to_tree2(
          (args, kwargs), prefix=(args_prefix, False),
        )

      extract.check_no_aliases('grad', args=args, kwargs=kwargs)

      fn_out = gradded_fn(*args, **kwargs)

      if return_value:
        if has_aux:
          (loss, (updates, aux)), grads = fn_out
          if graph: grads, aux = extract.from_tree2((grads, aux))
          result = (loss, aux), grads
        else:
          (loss, updates), grads = fn_out
          if graph: grads = extract.from_tree2(grads)
          result = loss, grads
      else:
        if has_aux:
          grads, (updates, aux) = fn_out
          if graph: grads, aux = extract.from_tree2((grads, aux))
          result = grads, aux
        else:
          grads, updates = fn_out
          if graph: grads = extract.from_tree2(grads)
          result = grads

      extract.apply_variable_updates((args, kwargs), updates)
      return result

    return tree_grad_wrapper

  jax_argnums: int | tuple[int, ...]
  if isinstance(argnums, (int, DiffState)):
    jax_argnums = argnums.argnum if isinstance(argnums, DiffState) else argnums
  else:
    jax_argnums = tuple(
      x.argnum if isinstance(x, DiffState) else x for x in argnums
    )

  _argnums = (argnums,) if isinstance(argnums, (int, DiffState)) else argnums
  index_filter: dict[int, DiffState] = {}
  for argnum in _argnums:
    index = argnum.argnum if isinstance(argnum, DiffState) else argnum
    if index in index_filter:
      raise ValueError(f'argnum {index} is repeated in argnums')
    index_filter[index] = (
      dataclasses.replace(argnum, argnum=-1)
      if isinstance(argnum, DiffState)
      else DiffState(-1, variablelib.Param)
    )

  @graphlib.update_context('grad')
  def grad_wrapper(*args, **kwargs):
    args = resolve_kwargs(f, args, kwargs)
    del kwargs
    nondiff_states: deque[State | variablelib.Variable | None] = deque()

    def _grad_split_fn(
      ctx: graphlib.SplitContext, path, prefix: DiffState | None, value
    ):
      if prefix is None or (prefix.argnum == -1 and isinstance(value, variablelib.Variable)):
        nondiff_states.append(None)
        return extract.NodeStates.from_split(*ctx.split(value))
      else:
        graphdef, diff, nondiff = ctx.split(value, prefix.filter, ...)  # type: ignore[misc]
        nondiff_states.append(nondiff)  # type: ignore[container-type-mismatch]
        return extract.NodeStates.from_split(graphdef, diff)

    arg_filters = tuple(index_filter.get(i) for i in range(len(args)))
    pure_args = extract.to_tree(
      args, prefix=arg_filters, split_fn=_grad_split_fn, ctxtag='grad'
    )

    gradded_fn = transform(
      GradFn(f, has_aux, nondiff_states),
      argnums=jax_argnums,
      has_aux=True,
      holomorphic=holomorphic,
      allow_int=allow_int,
    )

    fn_out = gradded_fn(*pure_args)

    def process_grads(grads):
      return jax.tree.map(
        lambda x: x.state if isinstance(x, extract.NodeStates) else x,
        grads,
        is_leaf=lambda x: isinstance(x, extract.NodeStates),
      )

    def process_out(pure_out: A, /) -> A:
      return extract.from_tree(pure_out, ctxtag='grad', is_inner=False)

    if return_value:
      # unpack value_and_grad output
      if has_aux:
        (loss, (pure_args_out, pure_aux)), grads = fn_out
        grads = process_grads(grads)
        _args_out, aux = process_out((pure_args_out, pure_aux))
        return (loss, aux), grads
      else:
        (loss, pure_args_out), grads = fn_out
        grads = process_grads(grads)
        _args_out = process_out(pure_args_out)
        return loss, grads
    else:
      # unpack grad output
      if has_aux:
        grads, (pure_args_out, pure_aux) = fn_out
        grads = process_grads(grads)
        _args_out, aux = process_out((pure_args_out, pure_aux))
        return grads, aux
      else:
        grads, pure_args_out = fn_out
        grads = process_grads(grads)
        _args_out = process_out(pure_args_out)
        return grads

  return grad_wrapper

