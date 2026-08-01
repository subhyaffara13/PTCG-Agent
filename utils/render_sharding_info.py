
def render_sharding_info(
    array_axis_info: Sequence[AxisInfo],
    sharding_info: ndarray_adapters.ShardingInfo,
    rows: Sequence[int | AxisName] = (),
    columns: Sequence[int | AxisName] = (),
) -> figures_impl.TreescopeFigure:
  """Renders the sharding of an array.

  This is a helper function for rendering array shardings. It can be used either
  to render the sharding of an actual array or of a hypothetical array of a
  given shape and sharding.

  Args:
    array_axis_info: Axis info for each axis of the array data.
    sharding_info: Sharding info for the array, as produced by a NDArrayAdapter.
    rows: Optional explicit ordering of rows in the visualization.
    columns: Optional explicit ordering of columns in the visualization.

  Returns:
    A rendering of the sharding, which re-uses the digitbox rendering mode to
    render sets of devices.
  """
  data_axis_from_axis_info = {
      info: axis for axis, info in enumerate(array_axis_info)
  }

  info_by_name_or_position = {}
  has_name_only = False
  positional_count = 0
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

  array_shape = [info.size for info in array_axis_info]
  orig_shard_shape = sharding_info.shard_shape
  num_shards = np.prod(array_shape) // np.prod(orig_shard_shape)
  orig_device_indices_map = sharding_info.device_index_to_shard_slices
  # Possibly adjust the shard shape so that its length is the same as the array
  # shape, and so that all items in device_indices_map are slices.
  device_indices_map = {}
  shard_shape = []
  orig_shard_shape_index = 0
  first = True
  for key, ints_or_slices in orig_device_indices_map.items():
    new_slices = []
    for i, int_or_slc in enumerate(ints_or_slices):
      if isinstance(int_or_slc, int):
        new_slices.append(slice(int_or_slc, int_or_slc + 1))
        if first:
          shard_shape.append(1)
      elif isinstance(int_or_slc, slice):
        new_slices.append(int_or_slc)
        if first:
          shard_shape.append(orig_shard_shape[orig_shard_shape_index])
          orig_shard_shape_index += 1
      else:
        raise ValueError(
            f"Unrecognized axis slice in sharding info: {int_or_slc} at index"
            f" {i} for device {key}"
        )
    device_indices_map[key] = tuple(new_slices)
    first = False

  assert len(shard_shape) == len(array_shape)
  assert orig_shard_shape_index == len(orig_shard_shape)
  # Compute a truncation for visualizing a single shard. Each shard will be
  # shown as a shrunken version of the actual shard dimensions, roughly
  # proportional to the shard sizes.
  mini_trunc = arrayviz_impl.infer_balanced_truncation(
      shape=array_shape,
      maximum_size=1000,
      cutoff_size_per_axis=10,
      minimum_edge_items=2,
      doubling_bonus=5,
  )
  # Infer an axis ordering.
  known_row_infos = [info_by_name_or_position[spec] for spec in rows]
  known_column_infos = [info_by_name_or_position[spec] for spec in columns]
  row_infos, column_infos = arrayviz_impl.infer_rows_and_columns(
      all_axes=array_axis_info,
      known_rows=known_row_infos,
      known_columns=known_column_infos,
      edge_items_per_axis=mini_trunc,
  )
  # Build an actual matrix to represent each shard, with a size determined by
  # the inferred truncation.
  shard_mask = np.ones((), dtype=np.bool_)
  for t, sh_s, arr_s in zip(mini_trunc, shard_shape, array_shape):
    if t is None or sh_s <= 5:
      vec = np.ones((sh_s,), dtype=np.bool_)
    else:
      candidate = t // (arr_s // sh_s)
      if candidate <= 2:
        vec = np.array([True] * 2 + [False] + [True] * 2)
      else:
        vec = np.array([True] * candidate + [False] + [True] * candidate)
    shard_mask = shard_mask[..., None] * vec
  # Figure out which device is responsible for each shard.
  device_to_shard_offsets = {}
  shard_offsets_to_devices = collections.defaultdict(list)
  for device_index, slices in device_indices_map.items():
    shard_offsets = []
    for i, slc in enumerate(slices):
      assert slc.step is None
      if slc.start is None:
        assert slc.stop is None
        shard_offsets.append(0)
      else:
        assert slc.stop == slc.start + shard_shape[i]
        shard_offsets.append(slc.start // shard_shape[i])

    shard_offsets = tuple(shard_offsets)
    device_to_shard_offsets[device_index] = shard_offsets
    shard_offsets_to_devices[shard_offsets].append(device_index)
  # Figure out what value to show for each shard. This determines the
  # visualization color.
  shard_offset_values = {}
  shard_value_descriptions = {}
  if len(device_indices_map) <= 10 and all(
      device_index < 10 for device_index in device_indices_map.keys()
  ):
    # Map each device to an integer digit 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, and
    # then draw replicas as collections of base-10 digits.
    for shard_offsets, shard_devices in shard_offsets_to_devices.items():
      if len(shard_devices) >= 7:
        # All devices are in the same shard! Arrayviz only supports 7 digits at
        # a time, so draw as much as we can.
        assert num_shards == 1
        vis_value = 1234567
      else:
        acc = 0
        for i, device_index in enumerate(shard_devices):
          acc += 10 ** (len(shard_devices) - i - 1) * (device_index + 1)
        vis_value = acc
      shard_offset_values[shard_offsets] = vis_value
      assert vis_value not in shard_value_descriptions
      shard_value_descriptions[vis_value] = (
          sharding_info.device_type
          + " "
          + ",".join(f"{d}" for d in shard_devices)
      )
    render_info_message = "Colored by device index."
  elif num_shards < 10:
    # More than ten devices, less than ten shards. Give each shard its own
    # index but start at 1.
    shard_offset_values = {
        shard_offsets: i + 1
        for i, shard_offsets in enumerate(shard_offsets_to_devices.keys())
    }
    render_info_message = "With a distinct pattern for each shard."
  else:
    # A large number of devices and shards. Start at 0.
    shard_offset_values = {
        shard_offsets: i
        for i, shard_offsets in enumerate(shard_offsets_to_devices.keys())
    }
    render_info_message = "With a distinct pattern for each shard."
  # Build the sharding visualization array.
  viz_shape = tuple(
      shard_mask.shape[i] * array_shape[i] // shard_shape[i]
      for i in range(len(array_shape))
  )
  dest = np.zeros(viz_shape, dtype=np.int32)
  destmask = np.empty(viz_shape, dtype=np.int32)
  shard_labels_by_vis_pos = [
      ["????" for _ in range(viz_shape[i])] for i in range(len(viz_shape))
  ]
  for shard_offsets, value in shard_offset_values.items():
    indexers = []
    for i, offset in enumerate(shard_offsets):
      vizslc = slice(
          offset * shard_mask.shape[i],
          (offset + 1) * shard_mask.shape[i],
          None,
      )
      indexers.append(vizslc)
      label = f"{offset * shard_shape[i]}:{(offset + 1) * shard_shape[i]}"
      for j in range(viz_shape[i])[vizslc]:
        shard_labels_by_vis_pos[i][j] = label
    dest[tuple(indexers)] = np.full_like(shard_mask, value, dtype=np.int32)
    destmask[tuple(indexers)] = shard_mask
  # Create formatting instructions to show what devices are in each shard.
  axis_lookups = [
      {
          "type": "axis_lookup",
          "axis": f"a{data_axis}",
          "skip_start": viz_shape[data_axis],
          "skip_end": viz_shape[data_axis],
          "lookup_table": {
              j: str(v)
              for j, v in enumerate(shard_labels_by_vis_pos[data_axis])
          },
      }
      for data_axis in range(len(array_shape))
  ]
  data_axis_labels = {}
  formatting_instructions = []
  formatting_instructions.append({"type": "literal", "value": "array"})

  if has_name_only:
    formatting_instructions.append({"type": "literal", "value": "[{"})

    first = True
    for data_axis, axis_info in enumerate(array_axis_info):
      if not isinstance(axis_info, NamedPositionlessAxisInfo):
        continue

      if first:
        formatting_instructions.append(
            {"type": "literal", "value": f"{repr(axis_info.axis_name)}:["}
        )
        first = False
      else:
        formatting_instructions.append(
            {"type": "literal", "value": f", {repr(axis_info.axis_name)}:["}
        )

      formatting_instructions.append(axis_lookups[data_axis])
      formatting_instructions.append({"type": "literal", "value": "]"})
      axshards = array_shape[data_axis] // shard_shape[data_axis]
      data_axis_labels[data_axis] = (
          f"{axis_info.axis_name}: {array_shape[data_axis]}/{axshards}"
      )
    formatting_instructions.append({"type": "literal", "value": "}]"})

  if positional_count:
    formatting_instructions.append({"type": "literal", "value": "["})
    for logical_index in range(positional_count):
      axis_info = info_by_name_or_position[logical_index]
      data_axis = data_axis_from_axis_info[axis_info]
      if logical_index:
        formatting_instructions.append({"type": "literal", "value": ", "})
      formatting_instructions.append(axis_lookups[data_axis])
      axshards = array_shape[data_axis] // shard_shape[data_axis]
      data_axis_labels[data_axis] = (
          f"axis {logical_index}: {array_shape[data_axis]}/{axshards}"
      )
    formatting_instructions.append({"type": "literal", "value": "]"})

  formatting_instructions.append({"type": "literal", "value": ":\n  "})
  formatting_instructions.append({
      "type": "value_lookup",
      "lookup_table": shard_value_descriptions,
      "ignore_invalid": True,
  })
  # Build the rendering.
  html_srcs = []
  html_srcs.append(
      arrayviz_impl.render_array_data_to_html(
          array_data=dest,
          valid_mask=destmask,
          column_axes=[data_axis_from_axis_info[c] for c in column_infos],
          row_axes=[data_axis_from_axis_info[r] for r in row_infos],
          slider_axes=(),
          axis_labels=[data_axis_labels[i] for i in range(len(array_shape))],
          vmin=0,
          vmax=0,
          cmap_type="digitbox",
          cmap_data=[],
          info=render_info_message,
          formatting_instructions=formatting_instructions,
          dynamic_continuous_cmap=False,
          raw_min_abs=0.0,
          raw_max_abs=0.0,
      )
  )
  html_srcs.append('<span style="font-family: monospace; white-space: pre">')
  for i, (shard_offsets, shard_devices) in enumerate(
      shard_offsets_to_devices.items()
  ):
    if i == 0:
      html_srcs.append(f"{sharding_info.device_type}")
    label = ",".join(f"{d}" for d in shard_devices)
    part = integer_digitbox(shard_offset_values[shard_offsets]).treescope_part
    assert isinstance(part, arrayviz_impl.ArrayvizDigitboxRendering)
    html_srcs.append(f"  {part.html_src} {label}")
  html_srcs.append("</span>")
  return figures_impl.TreescopeFigure(
      arrayviz_impl.ArrayvizRendering("".join(html_srcs))
  )

