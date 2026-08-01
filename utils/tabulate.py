
def tabulate(
    rows: list[tuple[str, Any]] | list[list[Any]],
    headers: tuple[str, ...] | list[str],
) -> str:
    try:
        import tabulate

        return tabulate.tabulate(rows, headers=headers)
    except ImportError:
        return "\n".join(
            ", ".join(map(str, row)) for row in itertools.chain([headers], rows)
        )


def tabulate(function, start=0):
    """Return an iterator over the results of ``func(start)``,
    ``func(start + 1)``, ``func(start + 2)``...

    *func* should be a function that accepts one integer argument.

    If *start* is not specified it defaults to 0. It will be incremented each
    time the iterator is advanced.

        >>> square = lambda x: x ** 2
        >>> iterator = tabulate(square, -3)
        >>> take(4, iterator)
        [9, 4, 1, 0]

    """
    return map(function, count(start))


def tabulate(rows: Iterable[Iterable[Any]]) -> tuple[list[str], list[int]]:
    """Return a list of formatted rows and a list of column sizes.
    For example::
    >>> tabulate([['foobar', 2000], [0xdeadbeef]])
    (['foobar     2000', '3735928559'], [10, 4])
    """
    rows = [tuple(map(str, row)) for row in rows]
    sizes = [max(map(_visible_len, col)) for col in zip_longest(*rows, fillvalue="")]
    table = [" ".join(map(_visible_ljust, row, sizes)).rstrip() for row in rows]
    return table, sizes


def tabulate(rows: Iterable[Iterable[Any]]) -> tuple[list[str], list[int]]:
    """Return a list of formatted rows and a list of column sizes.

    For example::

    >>> tabulate([['foobar', 2000], [0xdeadbeef]])
    (['foobar     2000', '3735928559'], [10, 4])
    """
    rows = [tuple(map(str, row)) for row in rows]
    sizes = [max(map(len, col)) for col in zip_longest(*rows, fillvalue="")]
    table = [" ".join(map(str.ljust, row, sizes)).rstrip() for row in rows]
    return table, sizes


def tabulate(
    rows: list[list[str | int]],
    headers: list[str],
    alignments: dict[str, str] | None = None,
) -> str:
    """
    Inspired by:

    - stackoverflow.com/a/8356620/593036
    - stackoverflow.com/questions/9535954/printing-lists-as-tabular-data
    """
    _ALIGN_MAP = {"left": "<", "right": ">"}
    for row in rows:
        if len(row) < len(headers):
            raise IndexError(f"Row has {len(row)} values but expected {len(headers)} (headers: {headers})")
    col_widths = [max(len(str(x)) for x in col) for col in zip(*rows, headers)]
    col_aligns = [_ALIGN_MAP.get((alignments or {}).get(h, "left"), "<") for h in headers]
    row_format = " ".join(f"{{:{a}{w}}}" for a, w in zip(col_aligns, col_widths))
    lines = []
    lines.append(row_format.format(*headers))
    lines.append(row_format.format(*["-" * w for w in col_widths]))
    for row in rows:
        lines.append(row_format.format(*row))
    return "\n".join(lines)


def tabulate(
  module: module_lib.Module,
  rngs: PRNGKey | RNGSequences,
  depth: int | None = None,
  show_repeated: bool = False,
  mutable: CollectionFilter = DenyList('intermediates'),
  console_kwargs: Mapping[str, Any] | None = None,
  table_kwargs: Mapping[str, Any] = MappingProxyType({}),
  column_kwargs: Mapping[str, Any] = MappingProxyType({}),
  compute_flops: bool = False,
  compute_vjp_flops: bool = False,
  **kwargs,
) -> Callable[..., str]:
  """Returns a function that creates a summary of the Module represented as a table.

  This function accepts most of the same arguments and internally calls
  `Module.init`, except that it returns a function of the form
  `(*args, **kwargs) -> str` where `*args` and `**kwargs` are passed to
  `method` (e.g. `__call__`) during the forward pass.

  `tabulate` uses `jax.eval_shape` under the hood to run the forward computation
  without consuming any FLOPs or allocating memory.

  Additional arguments can be passed into the `console_kwargs` argument, for
  example, `{'width': 120}`. For a full list of `console_kwargs` arguments, see:
  https://rich.readthedocs.io/en/stable/reference/console.html#rich.console.Console

  Example::

    >>> import flax.linen as nn
    >>> import jax, jax.numpy as jnp

    >>> class Foo(nn.Module):
    ...   @nn.compact
    ...   def __call__(self, x):
    ...     h = nn.Dense(4)(x)
    ...     return nn.Dense(2)(h)

    >>> x = jnp.ones((16, 9))
    >>> tabulate_fn = nn.tabulate(
    ...     Foo(), jax.random.key(0), compute_flops=True, compute_vjp_flops=True)

    >>> # print(tabulate_fn(x))

  This gives the following output::

                                           Foo Summary
    ┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
    ┃ path    ┃ module ┃ inputs        ┃ outputs       ┃ flops ┃ vjp_flops ┃ params          ┃
    ┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
    │         │ Foo    │ float32[16,9] │ float32[16,2] │ 1504  │ 4460      │                 │
    ├─────────┼────────┼───────────────┼───────────────┼───────┼───────────┼─────────────────┤
    │ Dense_0 │ Dense  │ float32[16,9] │ float32[16,4] │ 1216  │ 3620      │ bias:           │
    │         │        │               │               │       │           │ float32[4]      │
    │         │        │               │               │       │           │ kernel:         │
    │         │        │               │               │       │           │ float32[9,4]    │
    │         │        │               │               │       │           │                 │
    │         │        │               │               │       │           │ 40 (160 B)      │
    ├─────────┼────────┼───────────────┼───────────────┼───────┼───────────┼─────────────────┤
    │ Dense_1 │ Dense  │ float32[16,4] │ float32[16,2] │ 288   │ 840       │ bias:           │
    │         │        │               │               │       │           │ float32[2]      │
    │         │        │               │               │       │           │ kernel:         │
    │         │        │               │               │       │           │ float32[4,2]    │
    │         │        │               │               │       │           │                 │
    │         │        │               │               │       │           │ 10 (40 B)       │
    ├─────────┼────────┼───────────────┼───────────────┼───────┼───────────┼─────────────────┤
    │         │        │               │               │       │     Total │ 50 (200 B)      │
    └─────────┴────────┴───────────────┴───────────────┴───────┴───────────┴─────────────────┘

                                   Total Parameters: 50 (200 B)


  **Note**: rows order in the table does not represent execution order,
  instead it aligns with the order of keys in `variables` which are sorted
  alphabetically.

  **Note**: `vjp_flops` returns `0` if the module is not differentiable.

  Args:
    module: The module to tabulate.
    rngs: The rngs for the variable collections as passed to `Module.init`.
    depth: controls how many submodule deep the summary can go. By default its
      `None` which means no limit. If a submodule is not shown because of the
      depth limit, its parameter count and bytes will be added to the row of its
      first shown ancestor such that the sum of all rows always adds up to the
      total number of parameters of the Module.
    show_repeated: If `True`, repeated calls to the same module will be shown
      in the table, otherwise only the first call will be shown. Default is
      `False`.
    mutable: Can be bool, str, or list. Specifies which collections should be
      treated as mutable: ``bool``: all/no collections are mutable. ``str``: The
      name of a single mutable collection. ``list``: A list of names of mutable
      collections. By default all collections except 'intermediates' are
      mutable.
    console_kwargs: An optional dictionary with additional keyword arguments
      that are passed to `rich.console.Console` when rendering the table.
      Default arguments are `{'force_terminal': True, 'force_jupyter': False}`.
    table_kwargs: An optional dictionary with additional keyword arguments that
      are passed to `rich.table.Table` constructor.
    column_kwargs: An optional dictionary with additional keyword arguments that
      are passed to `rich.table.Table.add_column` when adding columns to the
      table.
    compute_flops: whether to include a `flops` column in the table listing the
      estimated FLOPs cost of each module forward pass. Does incur actual
      on-device computation / compilation / memory allocation, but still
      introduces overhead for large modules (e.g. extra 20 seconds for a
      Stable Diffusion's UNet, whereas otherwise tabulation would finish in 5
      seconds).
    compute_vjp_flops: whether to include a `vjp_flops` column in the table
      listing the estimated FLOPs cost of each module backward pass. Introduces
      a compute overhead of about 2-3X of `compute_flops`.
    **kwargs: Additional arguments passed to `Module.init`.

  Returns:
    A function that accepts the same `*args` and `**kwargs` of the forward pass
    (`method`) and returns a string with a tabular representation of the
    Modules.
  """
  # add non-default arguments to kwargs, this prevents some issue we overloading init
  # see: https://github.com/google/flax/issues/3299
  if mutable != DenyList('intermediates'):
    kwargs['mutable'] = mutable

  def _tabulate_fn(*fn_args, **fn_kwargs):
    table_fn = _get_module_table(
      module,
      depth=depth,
      show_repeated=show_repeated,
      compute_flops=compute_flops,
      compute_vjp_flops=compute_vjp_flops,
    )

    table = table_fn(rngs, *fn_args, **fn_kwargs, **kwargs)

    non_param_cols = [
      'path',
      'module',
      'inputs',
      'outputs',
    ]

    if compute_flops:
      non_param_cols.append('flops')
    if compute_vjp_flops:
      non_param_cols.append('vjp_flops')

    return _render_table(
      table, console_kwargs, table_kwargs, column_kwargs, non_param_cols
    )

  return _tabulate_fn


def tabulate(
  obj,
  *input_args,
  depth: int | None = None,
  method: str = '__call__',
  row_filter: tp.Callable[[CallInfo], bool] = filter_rng_streams,
  table_kwargs: tp.Mapping[str, tp.Any] = MappingProxyType({}),
  column_kwargs: tp.Mapping[str, tp.Any] = MappingProxyType({}),
  console_kwargs: tp.Mapping[str, tp.Any] = MappingProxyType({}),
  compute_flops: bool = False,
  compute_vjp_flops: bool = False,
  **input_kwargs,
) -> str:
  """Creates a summary of the graph object represented as a table.

  The table summarizes the object's state and metadata. The table is
  structured as follows:

  - The first column represents the path of the object in the graph.
  - The second column represents the type of the object.
  - The third column represents the input arguments passed to the object's
    method.
  - The fourth column represents the output of the object's method.
  - The following columns provide information about the object's state,
    grouped by Variable types.

  Example::

    >>> from flax import nnx
    ...
    >>> class Block(nnx.Module):
    ...   def __init__(self, din, dout, rngs: nnx.Rngs):
    ...     self.linear = nnx.Linear(din, dout, rngs=rngs)
    ...     self.bn = nnx.BatchNorm(dout, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.2, rngs=rngs)
    ...
    ...   def __call__(self, x):
    ...     return nnx.relu(self.dropout(self.bn(self.linear(x))))
    ...
    >>> class Foo(nnx.Module):
    ...   def __init__(self, rngs: nnx.Rngs):
    ...     self.block1 = Block(32, 128, rngs=rngs)
    ...     self.block2 = Block(128, 10, rngs=rngs)
    ...
    ...   def __call__(self, x):
    ...     return self.block2(self.block1(x))
    ...
    >>> foo = Foo(nnx.Rngs(0))
    >>> # print(nnx.tabulate(foo, jnp.ones((1, 32))))

                                                          Foo Summary
    ┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
    ┃ path           ┃ type      ┃ inputs         ┃ outputs        ┃ BatchStat          ┃ Param                   ┃ RngState ┃
    ┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
    │                │ Foo       │ float32[1,32]  │ float32[1,10]  │ 276 (1.1 KB)       │ 5,790 (23.2 KB)         │ 2 (12 B) │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block1         │ Block     │ float32[1,32]  │ float32[1,128] │ 256 (1.0 KB)       │ 4,480 (17.9 KB)         │ 2 (12 B) │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block1/linear  │ Linear    │ float32[1,32]  │ float32[1,128] │                    │ bias: float32[128]      │          │
    │                │           │                │                │                    │ kernel: float32[32,128] │          │
    │                │           │                │                │                    │                         │          │
    │                │           │                │                │                    │ 4,224 (16.9 KB)         │          │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block1/bn      │ BatchNorm │ float32[1,128] │ float32[1,128] │ mean: float32[128] │ bias: float32[128]      │          │
    │                │           │                │                │ var: float32[128]  │ scale: float32[128]     │          │
    │                │           │                │                │                    │                         │          │
    │                │           │                │                │ 256 (1.0 KB)       │ 256 (1.0 KB)            │          │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block1/dropout │ Dropout   │ float32[1,128] │ float32[1,128] │                    │                         │ 2 (12 B) │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block2         │ Block     │ float32[1,128] │ float32[1,10]  │ 20 (80 B)          │ 1,310 (5.2 KB)          │          │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block2/linear  │ Linear    │ float32[1,128] │ float32[1,10]  │                    │ bias: float32[10]       │          │
    │                │           │                │                │                    │ kernel: float32[128,10] │          │
    │                │           │                │                │                    │                         │          │
    │                │           │                │                │                    │ 1,290 (5.2 KB)          │          │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block2/bn      │ BatchNorm │ float32[1,10]  │ float32[1,10]  │ mean: float32[10]  │ bias: float32[10]       │          │
    │                │           │                │                │ var: float32[10]   │ scale: float32[10]      │          │
    │                │           │                │                │                    │                         │          │
    │                │           │                │                │ 20 (80 B)          │ 20 (80 B)               │          │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │ block2/dropout │ Dropout   │ float32[1,10]  │ float32[1,10]  │                    │                         │          │
    ├────────────────┼───────────┼────────────────┼────────────────┼────────────────────┼─────────────────────────┼──────────┤
    │                │           │                │          Total │ 276 (1.1 KB)       │ 5,790 (23.2 KB)         │ 2 (12 B) │
    └────────────────┴───────────┴────────────────┴────────────────┴────────────────────┴─────────────────────────┴──────────┘

                                                Total Parameters: 6,068 (24.3 KB)

  Note that ``block2/dropout`` is not shown in the table because it shares the
  same ``RngState`` with ``block1/dropout``.

  Args:
    obj: A object to summarize. It can a pytree or a graph objects
      such as nnx.Module or nnx.Optimizer.
    *input_args: Positional arguments passed to the object's method.
    **input_kwargs: Keyword arguments passed to the object's method.
    depth: The depth of the table.
    method: The method to call on the object. Default is ``'__call__'``.
    row_filter: A callable that filters the rows to be displayed in the table.
      By default, it filters out rows with type ``nnx.RngStream``.
    table_kwargs: An optional dictionary with additional keyword arguments
      that are passed to ``rich.table.Table`` constructor.
    column_kwargs: An optional dictionary with additional keyword arguments
      that are passed to ``rich.table.Table.add_column`` when adding columns to
      the table.
    console_kwargs: An optional dictionary with additional keyword arguments
      that are passed to `rich.console.Console` when rendering the table.
      Default arguments are  ``'force_terminal': True``, and ``'force_jupyter'``
      is set to ``True`` if the code is running in a Jupyter notebook, otherwise
      it is set to ``False``.
    compute_flops: whether to include a `flops` column in the table listing the
      estimated FLOPs cost of each module forward pass. Does incur actual
      on-device computation / compilation / memory allocation, but still
      introduces overhead for large modules (e.g. extra 20 seconds for a
      Stable Diffusion's UNet, whereas otherwise tabulation would finish in 5
      seconds).
    compute_vjp_flops: whether to include a `vjp_flops` column in the table
      listing the estimated FLOPs cost of each module backward pass. Introduces
      a compute overhead of about 2-3X of `compute_flops`.

  Returns:
    A string summarizing the object.
  """
  _console_kwargs = {'force_terminal': True, 'force_jupyter': in_ipython}
  _console_kwargs.update(console_kwargs)

  obj = graphlib.clone(obj)  # create copy to avoid side effects
  node_stats: NodeStats = {}
  object_types: set[type] = set()
  _collect_stats((), obj, node_stats, object_types)
  _variable_types: set[type] = {
    nnx.RngState  # type: ignore[misc]
    if isinstance(leaf, nnx.RngState)
    else type(leaf)
    for _, leaf in nnx.to_flat_state(nnx.state(obj))
  }
  variable_types: list[type] = sorted(_variable_types, key=lambda t: t.__name__)

  # Create a dictionary-version of the object's class. This makes
  # iteration over methods easier.
  env = _create_obj_env(object_types)

  # Information is recorded in post-order, but should be presented as a pre-order traversal.
  # This keeps track of the order of calls.
  counter = itertools.count(0)

  # Modify all the object's methods to save their lowered JIT representations.
  rows : list[CallInfo] = []
  seen : set = set()
  jits = {k: _save_call_info(counter, rows, v, node_stats, compute_flops, compute_vjp_flops, seen)
    for k, v in env.items()}
  _overwrite_methods(jits)

  # Trace the top function (which indirectly traces all the others)
  jits[(type(obj), method)](obj, *input_args, **input_kwargs)

  # Sort call info in pre-order traversal order
  rows.sort(key=lambda x: x.call_order)

  # Restore the object's original methods
  _overwrite_methods(env)

  if depth is not None:
    rows = [row for row in rows if len(row.path) <= depth and row_filter(row)]
  else:
    rows = [row for row in rows if row_filter(row)]

  rich_table = rich.table.Table(
    show_header=True,
    show_lines=True,
    show_footer=True,
    title=f'{type(obj).__name__} Summary',
    **table_kwargs,
  )

  rich_table.add_column('path', **column_kwargs)
  rich_table.add_column('type', **column_kwargs)
  rich_table.add_column('inputs', **column_kwargs)
  rich_table.add_column('outputs', **column_kwargs)
  if compute_flops:
    rich_table.add_column('flops', **column_kwargs)
  if compute_vjp_flops:
    rich_table.add_column('vjp_flops', **column_kwargs)

  for var_type in variable_types:
    rich_table.add_column(var_type.__name__, **column_kwargs)

  for row in rows:
    node_info = node_stats[row.object_id]
    assert node_info is not None
    col_reprs: list[str] = []
    path_str = '/'.join(map(str, row.path))
    col_reprs.append(path_str)
    col_reprs.append(row.type.__name__)
    col_reprs.append(row.inputs_repr)
    col_reprs.append(_as_yaml_str(row.outputs))
    if compute_flops:
      col_reprs.append(str(row.flops))
    if compute_vjp_flops:
      col_reprs.append(str(row.vjp_flops))

    for var_type in variable_types:
      attributes = {}
      variable: variablelib.Variable
      for name, variable in node_info.variable_groups[var_type].items():
        value = variable.get_value()
        value_repr = _render_array(value) if _has_shape_dtype(value) else ''
        metadata = variable.get_metadata()
        for required_key in var_type.required_metadata:
          metadata.pop(required_key, None)
        if metadata:
          attributes[name] = {
            'value': value_repr,
            **metadata,
          }
        elif value_repr:
          attributes[name] = value_repr  # type: ignore[assignment]

      if attributes:
        col_repr = _as_yaml_str(attributes) + '\n\n'
      else:
        col_repr = ''

      size_bytes = node_info.stats.get(var_type)  # type: ignore[call-overload]
      if size_bytes:
        col_repr += f'[bold]{size_bytes}[/bold]'
      col_reprs.append(col_repr)

    rich_table.add_row(*col_reprs)

  total_offset = 3 + int(compute_flops) + int(compute_vjp_flops)
  rich_table.columns[total_offset].footer = rich.text.Text.from_markup(
    'Total', justify='right'
  )
  node_info = node_stats[id(obj)]
  assert node_info is not None
  for i, var_type in enumerate(variable_types):
    size_bytes = node_info.stats[var_type]
    rich_table.columns[i + total_offset + 1].footer = str(size_bytes)

  rich_table.caption_style = 'bold'
  total_size = sum(node_info.stats.values(), SizeBytes(0, 0))
  rich_table.caption = f'\nTotal Parameters: {total_size}'

  return _get_rich_repr(rich_table, _console_kwargs)

