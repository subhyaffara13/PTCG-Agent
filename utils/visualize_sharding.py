
def visualize_sharding(dtensor, header="", use_rich: bool = False):
    """
    Visualizes sharding in the terminal for :class:`DTensor` that are 1D or 2D.

    .. note:: This requires the ``tabulate`` package, or ``rich`` and ``matplotlib``.
              No sharding info will be printed for empty tensors
    """
    if dtensor.numel() == 0:  # Do not print empty dtensors.
        return

    if len(dtensor.shape) >= 3:
        raise RuntimeError("visualize sharding supports only 1D or 2D DTensor")

    if dtensor.device_mesh.get_coordinate() is None:  # current rank is not in the mesh
        return

    # Only display the visualization once for each DTensor, on the rank whose
    # coordinate is 0 on all dimensions. For example, if the mesh is a full mesh,
    # we will only print on rank 0.
    local_rank_zero_on_all_dim = all(
        dtensor.device_mesh.get_local_rank(mesh_dim=dim) == 0
        for dim in range(dtensor.device_mesh.ndim)
    )
    if not local_rank_zero_on_all_dim:
        return

    device_coords = {
        int(device_index.item()): list(coord)
        for coord, device_index in np.ndenumerate(
            np.array(dtensor.device_mesh.mesh.tolist())
        )
    }

    device_shard_shape_and_offsets = {
        device_index: _compute_local_shape_and_global_offset(
            dtensor.shape,
            dtensor.device_mesh.shape,
            lambda i: device_coords[device_index][i],
            dtensor.placements,
        )
        for device_index in device_coords
    }

    # Extend shards in a 1D tensor to 2D
    device_shard_shape_and_offsets = {
        device_index: (
            shape if len(shape) == 2 else (shape[0], 1),
            offset if len(offset) == 2 else (offset[0], 0),
        )
        for device_index, (shape, offset) in device_shard_shape_and_offsets.items()
    }

    shards = [
        (
            (offset[0], offset[0] + shape[0] - 1),
            (offset[1], offset[1] + shape[1] - 1),
            device_index,
        )
        for device_index, (shape, offset) in device_shard_shape_and_offsets.items()
    ]

    if (
        importlib.util.find_spec("rich")
        and importlib.util.find_spec("matplotlib")
        and use_rich
    ):
        _create_rich_table(
            dtensor.shape, shards, device_kind=dtensor.device_mesh.device_type
        )
    elif importlib.util.find_spec("tabulate"):
        print(_create_table(shards, device_kind=dtensor.device_mesh.device_type))
    else:
        raise ValueError("`visualize_sharding` requires either `rich` or `tabulate`.")


def visualize_sharding(shape: Sequence[int], sharding: Sharding, *,
                       use_color: bool = True, scale: float = 1.,
                       min_width: int = 9, max_width: int = 80,
                       color_map: ColorMap | None = None):
  """Visualizes a ``Sharding`` using ``rich``."""
  if not importlib.util.find_spec("rich"):
    raise ValueError("`visualize_sharding` requires `rich` to be installed.")

  # These imports are local so that they don't affect JAX import times.
  import rich.align  # pyrefly: ignore[missing-import]
  import rich.console  # pyrefly: ignore[missing-import]
  import rich.box  # pyrefly: ignore[missing-import]
  import rich.padding  # pyrefly: ignore[missing-import]
  import rich.style  # pyrefly: ignore[missing-import]
  import rich.table  # pyrefly: ignore[missing-import]

  if len(shape) > 2 or len(shape) < 1:
    raise ValueError(
        "`visualize_sharding` only works for shapes with 1 and 2 dimensions.")
  console = rich.console.Console(width=max_width)
  use_color = use_color and console.color_system is not None
  if use_color and not color_map:
    try:
      import matplotlib as mpl  # pyrefly: ignore[missing-import]
      color_map = mpl.colormaps["tab20b"]
    except ModuleNotFoundError:
      use_color = False

  base_height = int(10 * scale)
  aspect_ratio = (shape[1] if len(shape) == 2 else 1) / shape[0]
  base_width = int(base_height * aspect_ratio)
  height_to_width_ratio = 2.5

  # Grab the device kind from the first device
  device_kind = next(iter(sharding.device_set)).platform.upper()

  device_indices_map = sharding.devices_indices_map(tuple(shape))
  slices: dict[tuple[int, ...], set[int]] = {}
  heights: dict[tuple[int, ...], float | None] = {}
  widths: dict[tuple[int, ...], float] = {}

  for i, (dev, slcs) in enumerate(device_indices_map.items()):
    assert slcs is not None
    slcs = tuple(map(_raise_to_slice, slcs))
    chunk_idxs = tuple(map(_slice_to_chunk_idx, shape, slcs))
    if slcs is None:
      raise NotImplementedError
    if len(slcs) == 2:
      vert, horiz = slcs
      vert_size  = ((vert.stop  - vert.start ) if vert.stop  is not None
                    else shape[0])
      horiz_size = ((horiz.stop - horiz.start) if horiz.stop is not None
                    else shape[1])
      chunk_height = vert_size / shape[0]
      chunk_width = horiz_size / shape[1]
      heights[chunk_idxs] = chunk_height
      widths[chunk_idxs] = chunk_width
    else:
      # In the 1D case, we set the height to 1.
      horiz, = slcs
      vert = slice(0, 1, None)
      horiz_size = (
          (horiz.stop - horiz.start) if horiz.stop is not None else shape[0])
      chunk_idxs = (0, *chunk_idxs)
      heights[chunk_idxs] = None
      widths[chunk_idxs]  = horiz_size / shape[0]
    slices.setdefault(chunk_idxs, set()).add(dev.id)
  num_rows = max(a[0] for a in slices.keys()) + 1
  if len(list(slices.keys())[0]) == 1:
    num_cols = 1
  else:
    num_cols = max(a[1] for a in slices.keys()) + 1

  color_iter = make_color_iter(color_map, num_rows, num_cols)
  table = rich.table.Table(show_header=False, show_lines=not use_color,
                           padding=0,
                           highlight=not use_color, pad_edge=False,
                           box=rich.box.SQUARE if not use_color else None)
  for i in range(num_rows):
    col = []
    for j in range(num_cols):
      entry = f"{device_kind} "+",".join([str(s) for s in sorted(slices[i, j])])
      width, maybe_height = widths[i, j], heights[i, j]
      width = int(width * base_width * height_to_width_ratio)
      if maybe_height is None:
        height = 1
      else:
        height = int(maybe_height * base_height)
      width = min(max(width, min_width), max_width)
      left_padding, remainder = divmod(width - len(entry) - 2, 2)
      right_padding = left_padding + remainder
      top_padding, remainder = divmod(height - 2, 2)
      bottom_padding = top_padding + remainder
      if use_color:
        color = _canonicalize_color(next(color_iter)[:3])
        text_color = _get_text_color(color)
        top_padding += 1
        bottom_padding += 1
        left_padding += 1
        right_padding += 1
      else:
        color = None
        text_color = None
      padding = (
          max(top_padding, 0),
          max(right_padding, 0),
          max(bottom_padding, 0),
          max(left_padding, 0),
      )
      col.append(
          rich.padding.Padding(
            rich.align.Align(entry, "center", vertical="middle"), padding,
            style=rich.style.Style(bgcolor=color,
              color=text_color)))
    table.add_row(*col)
  console.print(table, end='\n\n')

