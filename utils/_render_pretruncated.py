
def _render_pretruncated(
    *,
    array_axis_info: Sequence[AxisInfo],
    row_infos: Sequence[AxisInfo],
    column_infos: Sequence[AxisInfo],
    slider_infos: Sequence[AxisInfo],
    truncated_array_data: np.ndarray,
    truncated_mask_data: np.ndarray,
    edge_items_per_axis: Sequence[int | None],
    continuous: bool | Literal["auto"],
    around_zero: bool | Literal["auto"],
    vmax: float | None,
    vmin: float | None,
    trim_outliers: bool,
    dynamic_colormap: bool | Literal["auto"],
    colormap: list[tuple[int, int, int]] | None,
    axis_item_labels: dict[AxisName | int, list[str]] | None,
    value_item_labels: dict[int, str] | None,
    axis_labels: dict[AxisName | int, str] | None,
    pixels_per_cell: int | float = 7,
) -> arrayviz_impl.ArrayvizRendering:
  """Internal helper to render an array that has already been truncated."""
  if axis_item_labels is None:
    axis_item_labels = {}

  if value_item_labels is None:
    value_item_labels = {}

  if axis_labels is None:
    axis_labels = {}

  data_axis_from_axis_info = {
      info: axis for axis, info in enumerate(array_axis_info)
  }
  assert len(data_axis_from_axis_info) == len(array_axis_info)

  has_name_only = False
  positional_count = 0

  info_by_name_or_position = {}
  for info in array_axis_info:
    if isinstance(info, NamedPositionalAxisInfo):
      info_by_name_or_position[info.axis_name] = info
      info_by_name_or_position[info.axis_logical_index] = info
      positional_count += 1
    elif isinstance(info, PositionalAxisInfo):
      info_by_name_or_position[info.axis_logical_index] = info
      positional_count += 1
    elif isinstance(info, NamedPositionlessAxisInfo):
      info_by_name_or_position[info.axis_name] = info
      has_name_only = True
    else:
      raise ValueError(f"Unrecognized axis info {type(info)}")

  axis_labels_by_info = {
      info_by_name_or_position[orig_key]: value
      for orig_key, value in axis_labels.items()
  }
  axis_item_labels_by_info = {
      info_by_name_or_position[orig_key]: value
      for orig_key, value in axis_item_labels.items()
  }

  skip_start_indices = [
      edge_items if edge_items is not None else axis_info.size
      for edge_items, axis_info in zip(edge_items_per_axis, array_axis_info)
  ]
  skip_end_indices = [
      axis_info.size - edge_items if edge_items is not None else axis_info.size
      for edge_items, axis_info in zip(edge_items_per_axis, array_axis_info)
  ]

  # Convert the axis names into indices into our data array.
  column_data_axes = [
      data_axis_from_axis_info[orig_axis] for orig_axis in column_infos
  ]
  row_data_axes = [
      data_axis_from_axis_info[orig_axis] for orig_axis in row_infos
  ]
  slider_data_axes = [
      data_axis_from_axis_info[orig_axis] for orig_axis in slider_infos
  ]

  # Step 6: Figure out how to render the labels and indices of each axis.
  # We render indices using a small interpreted format language that can be
  # serialized to JSON and interpreted in JavaScript.
  data_axis_labels = {}
  formatting_instructions = []
  formatting_instructions.append({"type": "literal", "value": "array"})

  axis_label_instructions = []

  if has_name_only:
    formatting_instructions.append({"type": "literal", "value": "[{"})

    first = True
    for data_axis, axis_info in enumerate(array_axis_info):
      if not isinstance(axis_info, NamedPositionlessAxisInfo):
        continue

      if first:
        formatting_instructions.append(
            {"type": "literal", "value": f"{repr(axis_info.axis_name)}:"}
        )
        first = False
      else:
        formatting_instructions.append(
            {"type": "literal", "value": f", {repr(axis_info.axis_name)}:"}
        )

      formatting_instructions.append({
          "type": "index",
          "axis": f"a{data_axis}",
          "skip_start": skip_start_indices[data_axis],
          "skip_end": skip_end_indices[data_axis],
      })

      if axis_info in axis_labels_by_info:
        data_axis_labels[data_axis] = axis_labels_by_info[axis_info]
        label_name = f"{axis_labels_by_info[axis_info]} ({axis_info.axis_name})"
      elif axis_info in slider_infos:
        label_name = f"{str(axis_info.axis_name)}"
        data_axis_labels[data_axis] = label_name
      else:
        label_name = f"{str(axis_info.axis_name)}"
        data_axis_labels[data_axis] = f"{label_name}: {axis_info.size}"

      if axis_info in axis_item_labels_by_info:
        axis_label_instructions.extend([
            {"type": "literal", "value": f"\n{label_name} @ "},
            {
                "type": "index",
                "axis": f"a{data_axis}",
                "skip_start": skip_start_indices[data_axis],
                "skip_end": skip_end_indices[data_axis],
            },
            {"type": "literal", "value": ": "},
            {
                "type": "axis_lookup",
                "axis": f"a{data_axis}",
                "skip_start": skip_start_indices[data_axis],
                "skip_end": skip_end_indices[data_axis],
                "lookup_table": axis_item_labels_by_info[axis_info],
            },
        ])

    formatting_instructions.append({"type": "literal", "value": "}]"})

  if positional_count:
    formatting_instructions.append({"type": "literal", "value": "["})
    for logical_index in range(positional_count):
      axis_info = info_by_name_or_position[logical_index]
      assert isinstance(axis_info, PositionalAxisInfo | NamedPositionalAxisInfo)
      assert axis_info.axis_logical_index == logical_index
      data_axis = data_axis_from_axis_info[axis_info]
      if logical_index > 0:
        formatting_instructions.append({"type": "literal", "value": ", "})
      formatting_instructions.append({
          "type": "index",
          "axis": f"a{data_axis}",
          "skip_start": skip_start_indices[data_axis],
          "skip_end": skip_end_indices[data_axis],
      })

      if axis_info in axis_labels_by_info:
        data_axis_labels[data_axis] = axis_labels_by_info[axis_info]
        label_name = f"{axis_labels_by_info[axis_info]} (axis {logical_index})"
      else:
        if isinstance(axis_info, NamedPositionalAxisInfo):
          label_name = f"{axis_info.axis_name} (axis {logical_index})"
        else:
          label_name = f"axis {logical_index}"
        if axis_info in slider_infos:
          data_axis_labels[data_axis] = label_name
        else:
          data_axis_labels[data_axis] = f"{label_name}: {axis_info.size}"

      if axis_info in axis_item_labels_by_info:
        axis_label_instructions.extend([
            {"type": "literal", "value": f"\n{label_name} @ "},
            {
                "type": "index",
                "axis": f"a{data_axis}",
                "skip_start": skip_start_indices[data_axis],
                "skip_end": skip_end_indices[data_axis],
            },
            {"type": "literal", "value": ": "},
            {
                "type": "axis_lookup",
                "axis": f"a{data_axis}",
                "skip_start": skip_start_indices[data_axis],
                "skip_end": skip_end_indices[data_axis],
                "lookup_table": axis_item_labels_by_info[axis_info],
            },
        ])

    formatting_instructions.append({"type": "literal", "value": "]"})

  formatting_instructions.append({"type": "literal", "value": "\n  = "})
  formatting_instructions.append({"type": "value"})

  # Step 7: Infer the colormap and rendering strategy.

  # Figure out whether the array is continuous.
  inferred_continuous = dtype_util.is_floating_dtype(truncated_array_data.dtype)
  if continuous == "auto":
    continuous = inferred_continuous
  elif not continuous and inferred_continuous:
    raise ValueError(
        "Cannot use continuous=False when rendering a float array; explicitly"
        " cast it to an integer array first."
    )

  if inferred_continuous:
    # Cast to float32 to ensure we can easily manipulate the truncated data.
    truncated_array_data = truncated_array_data.astype(np.float32)

  if value_item_labels and not continuous:
    formatting_instructions.append({"type": "literal", "value": "  # "})
    formatting_instructions.append(
        {"type": "value_lookup", "lookup_table": value_item_labels}
    )

  formatting_instructions.extend(axis_label_instructions)

  # Figure out centering.
  definitely_not_around_zero = (
      vmin is not None and vmax is not None and vmin != -vmax  # pylint: disable=invalid-unary-operand-type
  )
  if around_zero == "auto":
    around_zero = not definitely_not_around_zero
  elif around_zero and definitely_not_around_zero:
    raise ValueError(
        "Cannot use around_zero=True while also specifying both vmin and vmax"
    )

  # Check whether we should dynamically adjust the colormap.
  if dynamic_colormap == "auto":
    dynamic_colormap = (
        continuous and around_zero and vmin is None and vmax is None
    )

  if dynamic_colormap:
    if not continuous:
      raise ValueError(
          "Cannot use dynamic_colormap with a non-continuous colormap."
      )
    if not around_zero:
      raise ValueError("Cannot use dynamic_colormap without around_zero.")

    raw_min_abs, raw_max_abs = arrayviz_impl.infer_abs_min_max(
        truncated_array_data, truncated_mask_data
    )
    raw_min_abs = float(raw_min_abs)
    raw_max_abs = float(raw_max_abs)
  else:
    raw_min_abs = None
    raw_max_abs = None

  # Infer concrete `vmin` and `vmax`.
  if continuous and (vmin is None or vmax is None):
    vmin, vmax = arrayviz_impl.infer_vmin_vmax(
        array=truncated_array_data,
        mask=truncated_mask_data,
        vmin=vmin,
        vmax=vmax,
        around_zero=around_zero,
        trim_outliers=trim_outliers,
    )
    vmin = float(vmin)
    vmax = float(vmax)

  # Figure out which colormap and rendering strategy to use.
  if colormap is None:
    if continuous:
      colormap_type = "continuous"
      if around_zero:
        colormap_data = default_diverging_colormap.get()
      else:
        colormap_data = default_sequential_colormap.get()

    else:
      colormap_type = "digitbox"
      colormap_data = []

  elif continuous:
    colormap_data = colormap
    colormap_type = "continuous"

  else:
    colormap_data = colormap
    colormap_type = "palette_index"

  # Make a title for it
  info_parts = []
  if dynamic_colormap:
    info_parts.append("Dynamic colormap (click to adjust).")
  elif continuous:
    info_parts.append(f"Linear colormap from {vmin:.6g} to {vmax:.6g}.")
  elif colormap is not None:
    info_parts.append("Indexed colors from a color list.")
  else:
    info_parts.append("Showing integer digits as nested squares.")

  info_parts.append(" Hover/click for array data.")

  # Step 8: Render it!
  html_src = arrayviz_impl.render_array_data_to_html(
      array_data=truncated_array_data,
      valid_mask=truncated_mask_data,
      column_axes=column_data_axes,
      row_axes=row_data_axes,
      slider_axes=slider_data_axes,
      axis_labels=[
          data_axis_labels[i] for i in range(truncated_array_data.ndim)
      ],
      vmin=vmin,
      vmax=vmax,
      cmap_type=colormap_type,
      cmap_data=colormap_data,
      info="".join(info_parts),
      formatting_instructions=formatting_instructions,
      dynamic_continuous_cmap=dynamic_colormap,
      raw_min_abs=raw_min_abs,
      raw_max_abs=raw_max_abs,
      pixels_per_cell=pixels_per_cell,
  )
  return arrayviz_impl.ArrayvizRendering(html_src)

