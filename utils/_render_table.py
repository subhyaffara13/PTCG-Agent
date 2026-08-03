from typing import Any

def _render_table(
  table: Table,
  console_extras: Mapping[str, Any] | None,
  table_kwargs: Mapping[str, Any],
  column_kwargs: Mapping[str, Any],
  non_params_cols: list[str],
) -> str:
  """A function that renders a Table to a string representation using rich."""
  console_kwargs = {'force_terminal': True, 'force_jupyter': False}
  if console_extras is not None:
    console_kwargs.update(console_extras)

  rich_table = rich.table.Table(
    show_header=True,
    show_lines=True,
    show_footer=True,
    title=f'{table.module.__class__.__name__} Summary',
    **table_kwargs,
  )

  for c in non_params_cols:
    rich_table.add_column(c, **column_kwargs)

  for col in table.collections:
    rich_table.add_column(col, **column_kwargs)

  for row in table:
    collections_size_repr = []

    for collection, size_bytes in row.size_and_bytes(table.collections).items():
      col_repr = ''

      if collection in row.module_variables:
        module_variables = _represent_tree(row.module_variables[collection])
        module_variables = _normalize_structure(module_variables)
        col_repr += _as_yaml_str(
          _summary_tree_map(_maybe_render, module_variables)
        )
        if col_repr:
          col_repr += '\n\n'

      col_repr += f'[bold]{_size_and_bytes_repr(*size_bytes)}[/bold]'
      collections_size_repr.append(col_repr)

    no_show_methods = {'__call__', '<lambda>'}
    path_repr = '/'.join(row.path)
    method_repr = (
      f' [dim]({row.method})[/dim]' if row.method not in no_show_methods else ''
    )
    rich_table.add_row(
      path_repr,
      type(row.module_copy).__name__ + method_repr,
      *(
        _as_yaml_str(
          _summary_tree_map(
            _maybe_render, _normalize_structure(getattr(row, c))
          )
        )
        for c in non_params_cols[2:]
      ),
      *collections_size_repr,
    )

  # add footer with totals
  n_non_params_cols = len(non_params_cols)
  rich_table.columns[n_non_params_cols - 1].footer = rich.text.Text.from_markup(
    'Total', justify='right'
  )

  # get collection totals
  collection_total = {col: (0, 0) for col in table.collections}
  for row in table:
    for col, size_bytes in row.size_and_bytes(table.collections).items():
      collection_total[col] = (
        collection_total[col][0] + size_bytes[0],
        collection_total[col][1] + size_bytes[1],
      )

  # add totals to footer
  for i, col in enumerate(table.collections):
    rich_table.columns[n_non_params_cols + i].footer = _size_and_bytes_repr(
      *collection_total[col]
    )

  # add final totals to caption
  caption_totals = (0, 0)
  for size, num_bytes in collection_total.values():
    caption_totals = (
      caption_totals[0] + size,
      caption_totals[1] + num_bytes,
    )

  rich_table.caption_style = 'bold'
  rich_table.caption = (
    f'\nTotal Parameters: {_size_and_bytes_repr(*caption_totals)}'
  )

  return '\n' + _get_rich_repr(rich_table, console_kwargs) + '\n'

