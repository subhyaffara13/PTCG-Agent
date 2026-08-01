
def infer_rows_and_columns(
    all_axes: Sequence[AxisInfo],
    known_rows: Sequence[AxisInfo] = (),
    known_columns: Sequence[AxisInfo] = (),
    edge_items_per_axis: tuple[int | None, ...] | None = None,
) -> tuple[list[AxisInfo], list[AxisInfo]]:
  """Infers an ordered assignment of axis indices or names to rows and columns.

  The unassigned axes are sorted by size and then assigned to rows and columns
  to try to balance the total number of elements along the row and column axes.
  This currently uses a greedy algorithm with an adjustment to try to keep
  columns longer than rows, except when there are exactly two axes and both are
  positional, in which case it lays out axis 0 as the rows and axis 1 as the
  columns.

  Axes with logical positions are sorted before axes with only names
  (in reverse order, so that later axes are rendered on the inside). Axes with
  names only appear afterward, with explicitly-assigned ones before unassigned
  ones.

  Args:
    all_axes: Sequence of axis infos in the array that should be assigned.
    known_rows: Sequence of axis indices or names that must map to rows.
    known_columns: Sequence of axis indices or names that must map to columns.
    edge_items_per_axis: Optional edge items specification, determining
      truncated size of each axis. Must match the ordering of `all_axes`.

  Returns:
    Tuple (rows, columns) of assignments, which consist of `known_rows` and
    `known_columns` followed by the remaining unassigned axes in a balanced
    order.
  """
  if edge_items_per_axis is None:
    edge_items_per_axis = (None,) * len(all_axes)

  if not known_rows and not known_columns and len(all_axes) == 2:
    ax_a, ax_b = all_axes
    if (
        isinstance(ax_a, PositionalAxisInfo)
        and isinstance(ax_b, PositionalAxisInfo)
        and {ax_a.axis_logical_index, ax_b.axis_logical_index} == {0, 1}
    ):
      # Two-dimensional positional array. Always do rows then columns.
      if ax_a.axis_logical_index == 0:
        return ([ax_a], [ax_b])
      else:
        return ([ax_b], [ax_a])

  truncated_sizes = {
      ax: ax.size if edge_items is None else 2 * edge_items + 1
      for ax, edge_items in zip(all_axes, edge_items_per_axis)
  }
  unassigned = [
      ax for ax in all_axes if ax not in known_rows and ax not in known_columns
  ]

  # Sort by size descending, so that we make the most important layout decisions
  # first.
  unassigned = sorted(
      unassigned, key=lambda ax: (truncated_sizes[ax], ax.size), reverse=True
  )

  # Compute the total size every axis would have if we assigned them to the
  # same axis.
  unassigned_size = np.prod([truncated_sizes[ax] for ax in unassigned])

  rows = list(known_rows)
  row_size = np.prod([truncated_sizes[ax] for ax in rows])
  columns = list(known_columns)
  column_size = np.prod([truncated_sizes[ax] for ax in columns])

  for ax in unassigned:
    axis_size = truncated_sizes[ax]
    unassigned_size = unassigned_size // axis_size
    if row_size * axis_size > column_size * unassigned_size:
      # If we assign this to the row axis, we'll end up with a visualization
      # with more rows than columns regardless of what we do later, which can
      # waste screen space. Assign to columns instead.
      columns.append(ax)
      column_size *= axis_size
    else:
      # Assign to the row axis. We'll assign columns later.
      rows.append(ax)
      row_size *= axis_size

  # The specific ordering of axes along the rows and the columns is somewhat
  # arbitrary. Re-order each so that explicitly requested axes are first, then
  # unassigned positional axes in reverse position order, then unassigned named
  # axes.
  def ax_sort_key(ax: AxisInfo):
    if ax not in unassigned:
      return (0,)
    elif isinstance(ax, PositionalAxisInfo | NamedPositionalAxisInfo):
      return (1, -ax.axis_logical_index)
    else:
      return (2,)

  return sorted(rows, key=ax_sort_key), sorted(columns, key=ax_sort_key)

