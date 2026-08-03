import functools

def transform_metadata(
    *,
    in_axes: tp.Any = 0,
    out_axes: tp.Any = 0,
    partition: str | None,
    graph: bool | None = None,
) -> tp.Callable[[F], F]:
  ...


def transform_metadata(
    f: F,
    *,
    in_axes: tp.Any = 0,
    out_axes: tp.Any = 0,
    graph: bool | None = None,
    partition: str | None,
) -> F:
  ...


def transform_metadata(
    f: F | type[Missing] = Missing,
    *,
    in_axes: tp.Any = 0,
    out_axes: tp.Any = 0,
    partition: str | None,
    graph: bool | None = None,
) -> F | tp.Callable[[F], F]:
  if f is Missing:
    return functools.partial(
        transform_metadata,
        in_axes=in_axes,
        out_axes=out_axes,
        partition=partition,
        graph=graph,
    )  # type: ignore[return-value]

  if graph is None:
    graph = graphlib.set_graph_mode.current_value()

  metadata: tp.Mapping[str, tp.Any] = {
      spmd.PARTITION_NAME: partition,
  }
  extract.check_prefix(in_axes, 'in_axes', 'transform_metadata', graph, True)
  extract.check_prefix(out_axes, 'out_axes', 'transform_metadata', graph, True)

  @functools.wraps(f)
  def wrapper(*in_args, **in_kwargs):
    in_args = resolve_kwargs(f, in_args, in_kwargs)
    if graph:
      in_args = extract.to_tree2(in_args, prefix=in_axes)
    extract.check_no_aliases('transform_metadata', args=in_args)
    args = graphlib.clone(in_args, graph=graph)
    _apply_axis_fn(args, in_axes, metadata, spmd.remove_axis)
    updates, snapshot = extract.updates_and_snapshot(args)
    if graph:
      args = extract.from_tree2(args)
    out = f(*args)
    if graph:
      out = extract.to_tree2(out, prefix=out_axes)
    extract.check_no_aliases(
        'transform_metadata', args=updates, out=out, check_can_update=['out']
    )
    _apply_axis_fn(args, in_axes, metadata, spmd.add_axis)
    _apply_axis_fn(out, out_axes, metadata, spmd.add_axis)
    updates = extract.mask_variable_updates(updates, snapshot)
    extract.apply_variable_updates(in_args, updates)
    if graph:
      out = extract.from_tree2(out)
    return out

  return wrapper  # type: ignore[return-value]

