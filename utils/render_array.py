
def render_array(
    array: ArrayInRegistry,
    *,
    columns: Sequence[AxisName | int] = (),
    rows: Sequence[AxisName | int] = (),
    sliders: Sequence[AxisName | int] = (),
    valid_mask: Any | None = None,
    continuous: bool | Literal["auto"] = "auto",
    around_zero: bool | Literal["auto"] = "auto",
    vmax: float | None = None,
    vmin: float | None = None,
    trim_outliers: bool = True,
    dynamic_colormap: bool | Literal["auto"] = "auto",
    colormap: list[tuple[int, int, int]] | None = None,
    truncate: bool = False,
    maximum_size: int = 10_000,
    cutoff_size_per_axis: int = 512,
    minimum_edge_items: int = 5,
    axis_item_labels: dict[AxisName | int, list[str]] | None = None,
    value_item_labels: dict[int, str] | None = None,
    axis_labels: dict[AxisName | int, str] | None = None,
    pixels_per_cell: int | float = 7,
) -> figures_impl.TreescopeFigure:
  """Renders an array (positional or named) to a displayable HTML object.

  Each element of the array is rendered to a fixed-size square, with its
  position determined based on its index, and with each level of x and y axis
  represented by a "faceted" plot.

  Out-of-bounds or otherwise unusual data is rendered with an annotation:

  * "X" means a value was NaN (for continuous data) or went out-of-bounds for
    the integer palette (for discrete data).

  * "I" or "-I" means a value was infinity or negative infinity.

  * "+" or "-" means a value was finite but went outside the bounds of the
    colormap (e.g. it was larger than ``vmax`` or smaller than ``vmin``). By
    default this applies to values more than 3 standard deviations outside the
    mean.

  * Four light dots on grey means a value was masked out by ``valid_mask``, or
    truncated due to the maximum size or axis cutoff thresholds.

  By default, this method automatically chooses a color rendering strategy based
  on the arguments:

  * If an explicit colormap is provided:

    * If ``continuous`` is True, the provided colors are interpreted as color
      stops and interpolated between.

    * If ``continuous`` is False, the provided colors are interpreted as an
      indexed color palette, and each index of the palette is used to render
      the corresponding integer, starting from zero.

  * Otherwise:

    * If ``continuous`` is True:

      * If ``around_zero`` is True, uses the diverging colormap
        `default_diverging_colormap`. The initial value of this is a truncated
        version of the perceptually-uniform "Balance" colormap from cmocean,
        with blue for positive numbers and red for negative ones.

      * If ``around_zero`` is False, uses the sequential colormap
        `default_sequential_colormap`.The initial value of this is the
        perceptually-uniform "Viridis" colormap from matplotlib.

    * If ``continuous`` is False, uses a pattern-based "digitbox" rendering
      strategy to render integers up to 9,999,999 as nested squares, with one
      square per integer digit and digit colors drawn from the D3 Category20
      colormap.

  Args:
      array: The array to render. The type of this array must be registered in
        the `type_registries.NDARRAY_ADAPTER_REGISTRY`.
      columns: Sequence of axis names or positional axis indices that should be
        placed on the x axis, from innermost to outermost. If not provided,
        inferred automatically.
      rows: Sequence of axis names or positional axis indices that should be
        placed on the y axis, from innermost to outermost. If not provided,
        inferred automatically.
      sliders: Sequence of axis names or positional axis indices for which we
        should show only a single slice at a time, with the index determined
        with a slider.
      valid_mask: Optionally, a boolean array with the same shape (and, if
        applicable, axis names) as `array`, which is True for the locations that
        we should actually render, and False for locations that do not have
        valid array data.
      continuous: Whether to interpret this array as numbers along the real
        line, and visualize using an interpolated colormap. If "auto", inferred
        from the dtype of `array`.
      around_zero: Whether the array data should be rendered symmetrically
        around zero using a diverging colormap, scaled based on the absolute
        magnitude of the inputs, instead of rescaled to be between the min and
        max of the data. If "auto", treated as True unless both `vmin` and
        `vmax` are set to incompatible values.
      vmax: Largest value represented in the colormap. If omitted and
        around_zero is True, inferred as ``max(abs(array))`` or as ``-vmin``. If
        omitted and around_zero is False, inferred as ``max(array)``.
      vmin: Smallest value represented in the colormap. If omitted and
        around_zero is True, inferred as ``-max(abs(array))`` or as ``-vmax``.
        If omitted and around_zero is False, inferred as ``min(array)``.
      trim_outliers: Whether to try to trim outliers when inferring ``vmin`` and
        ``vmax``. If True, clips them to 3 standard deviations away from the
        mean (or 3 sqrt-second-moments around zero) if they would otherwise
        exceed it.
      dynamic_colormap: Whether to dynamically adjust the colormap based on
        mouse hover. Requires a continuous colormap, and ``around_zero=True``.
        If "auto", will be enabled for continuous arrays if ``around_zero`` is
        True and neither ``vmin`` nor ``vmax`` are provided.
      colormap: An optional explicit colormap to use, represented as a list of
        ``(r,g,b)`` tuples, where each channel is between 0 and 255. A good
        place to get colormaps is the ``palettable`` package, e.g. you can pass
        something like ``palettable.matplotlib.Inferno_20.colors``.
      truncate: Whether or not to truncate the array to a smaller size before
        rendering.
      maximum_size: Maximum number of elements of an array to show. Arrays
        larger than this will be truncated along one or more axes. Ignored
        unless ``truncate`` is True.
      cutoff_size_per_axis: Maximum number of elements of each individual axis
        to show without truncation. Any axis longer than this will be truncated,
        with their visual size increasing logarithmically with the true axis
        size beyond this point. Ignored unless ``truncate`` is True.
      minimum_edge_items: How many values to keep along each axis for truncated
        arrays. We may keep more than this up to the budget of maximum_size.
        Ignored unless ``truncate`` is True.
      axis_item_labels: An optional mapping from axis names/positions to a list
        of strings, of the same length as the axis length, giving a label to
        each item along that axis. For instance, this could be the token string
        corresponding to each position along a sequence axis, or the class label
        corresponding to each category across a classifier's output axis. This
        is shown in the tooltip when hovering over a pixel, and shown below the
        array when a pixel is clicked on. For convenience, names in this
        dictionary that don't match any axes in the input are simply ignored, so
        that you can pass the same labels while rendering arrays that may not
        have the same axis names.
      value_item_labels: For categorical data, an optional mapping from each
        value to a string. For instance, this could be the token value
        corresponding to each token ID in a sequence of tokens.
      axis_labels: Optional mapping from axis names / indices to the labels we
        should use for that axis. If not provided, we label the named axes with
        their names and the positional axes with "axis {i}", and also add th
        axis size.
      pixels_per_cell: Size of each rendered array element in pixels, between 1
        and 21 inclusive. This controls the zoom level of the rendering. Array
        elements are always drawn at 7 pixels per cell and then rescaled, so
        out-of-bounds annotations and "digitbox" integer value patterns may not
        display correctly at fewer than 7 pixels per cell.

  Returns:
    An object which can be rendered in an IPython notebook, containing the
    HTML source of an arrayviz rendering.
  """
  # Retrieve the adapter for this array, which we will use to construct
  # the rendering.
  type_registries.update_registries_for_imports()
  adapter = type_registries.lookup_ndarray_adapter(array)
  if adapter is None:
    raise TypeError(
        f"Cannot render array with unrecognized type {type(array)} (not found"
        " in array adapter registry)"
    )
  if not 1 <= pixels_per_cell <= 21:
    raise ValueError(
        "pixels_per_cell must be between 1 and 21 inclusive, got"
        f" {pixels_per_cell}"
    )

  # Extract information about axis names, indices, and sizes.
  array_axis_info = adapter.get_axis_info_for_array_data(array)

  data_axis_from_axis_info = {
      info: axis for axis, info in enumerate(array_axis_info)
  }
  assert len(data_axis_from_axis_info) == len(array_axis_info)

  info_by_name_or_position = {}
  for info in array_axis_info:
    if isinstance(info, NamedPositionalAxisInfo):
      info_by_name_or_position[info.axis_name] = info
      info_by_name_or_position[info.axis_logical_index] = info
    elif isinstance(info, PositionalAxisInfo):
      info_by_name_or_position[info.axis_logical_index] = info
    elif isinstance(info, NamedPositionlessAxisInfo):
      info_by_name_or_position[info.axis_name] = info
    else:
      raise ValueError(f"Unrecognized axis info {type(info)}")

  row_infos = [info_by_name_or_position[spec] for spec in rows]
  column_infos = [info_by_name_or_position[spec] for spec in columns]
  slider_infos = [info_by_name_or_position[spec] for spec in sliders]

  unassigned_axes = set(array_axis_info)
  seen_axes = set()
  for axis_info in itertools.chain(row_infos, column_infos, slider_infos):
    if axis_info in seen_axes:
      raise ValueError(
          f"Axis {axis_info} appeared multiple times in rows/columns/sliders"
          " specifications. Each axis must be assigned to at most one"
          " location."
      )
    seen_axes.add(axis_info)
    unassigned_axes.remove(axis_info)

  if truncate:
    # Infer a good truncated shape for this array.
    edge_items_per_axis = arrayviz_impl.infer_balanced_truncation(
        tuple(info.size for info in array_axis_info),
        maximum_size=maximum_size,
        cutoff_size_per_axis=cutoff_size_per_axis,
        minimum_edge_items=minimum_edge_items,
    )
  else:
    edge_items_per_axis = (None,) * len(array_axis_info)

  # Obtain truncated array and mask data from the adapter.
  truncated_array_data, truncated_mask_data = (
      adapter.get_array_data_with_truncation(
          array=array,
          mask=valid_mask,
          edge_items_per_axis=edge_items_per_axis,
      )
  )

  # Step 5: Figure out which axes to render as rows, columns, and sliders and
  # in which order. We start with the explicitly-requested axes, then add more
  # axes to the rows and columns until we've assigned all of them, trying to
  # balance rows and columns.

  row_infos, column_infos = arrayviz_impl.infer_rows_and_columns(
      all_axes=[ax for ax in array_axis_info if ax not in slider_infos],
      known_rows=row_infos,
      known_columns=column_infos,
      edge_items_per_axis=edge_items_per_axis,
  )

  return figures_impl.TreescopeFigure(
      _render_pretruncated(
          array_axis_info=array_axis_info,
          row_infos=row_infos,
          column_infos=column_infos,
          slider_infos=slider_infos,
          truncated_array_data=truncated_array_data,
          truncated_mask_data=truncated_mask_data,
          edge_items_per_axis=edge_items_per_axis,
          continuous=continuous,
          around_zero=around_zero,
          vmax=vmax,
          vmin=vmin,
          trim_outliers=trim_outliers,
          dynamic_colormap=dynamic_colormap,
          colormap=colormap,
          axis_item_labels=axis_item_labels,
          value_item_labels=value_item_labels,
          axis_labels=axis_labels,
          pixels_per_cell=pixels_per_cell,
      )
  )

