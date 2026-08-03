import json
from typing import Any

def render_array_data_to_html(
    array_data: np.ndarray,
    valid_mask: np.ndarray,
    column_axes: Sequence[int],
    row_axes: Sequence[int],
    slider_axes: Sequence[int],
    axis_labels: list[str],
    vmin: float,
    vmax: float,
    cmap_type: Literal["continuous", "palette_index", "digitbox"],
    cmap_data: list[tuple[int, int, int]],
    info: str = "",
    formatting_instructions: list[dict[str, Any]] | None = None,
    dynamic_continuous_cmap: bool = False,
    raw_min_abs: float | None = None,
    raw_max_abs: float | None = None,
    pixels_per_cell: int | float = 7,
) -> str:
  """Helper to render an array to HTML by passing arguments to javascript.

  Args:
    array_data: Array data to render.
    valid_mask: Mask array, of same shape as array_data, that is True for items
      we should render.
    column_axes: Axes (by index into `array_data`) to arrange as columns,
      ordered from outermost group to innermost group.
    row_axes: Axes (by index into `array_data`) to arrange as rows, ordered from
      outermost group to innermost group.
    slider_axes: Axes to bind to sliders.
    axis_labels: Labels for each axis.
    vmin: Minimum for the colormap.
    vmax: Maximum for the colormap.
    cmap_type: Type of colormap (see `render_array`)
    cmap_data: Data for the colormap, as a sequence of RGB triples.
    info: Info for the plot.
    formatting_instructions: Formatting instructions for values on mouse hover
      or click. These will be interpreted by `formatValueAndIndices` on the
      JavaScript side. Can assume each axis is named "a0", "a1", etc. when
      running in JavaScript.
    dynamic_continuous_cmap: Whether to dynamically adjust the colormap during
      rendering.
    raw_min_abs: Minimum absolute value of the array, for dynamic remapping.
    raw_max_abs: Maximum absolute value of the array, for dynamic remapping.
    pixels_per_cell: The initial number of pixels per cell when rendering.

  Returns:
    HTML source for an arrayviz rendering.
  """
  assert len(array_data.shape) == len(axis_labels)
  assert len(valid_mask.shape) == len(axis_labels)

  if formatting_instructions is None:
    formatting_instructions = [{"type": "value"}]

  # Compute strides for each axis. We refer to each axis as "a0", "a1", etc
  # across the JavaScript boundary.
  stride = 1
  strides = {}
  for i, axis_size in reversed(list(enumerate(array_data.shape))):
    strides[f"a{i}"] = stride
    stride *= axis_size

  if cmap_type == "continuous":
    converted_array_data = array_data.astype(np.float32)
    array_dtype = "float32"
  else:
    converted_array_data = array_data.astype(np.int32)
    array_dtype = "int32"

  def axis_spec_arg(i):
    return {
        "name": f"a{i}",
        "label": axis_labels[i],
        "start": 0,
        "end": array_data.shape[i],
    }

  x_axis_specs_arg = []
  for axis in column_axes:
    x_axis_specs_arg.append(axis_spec_arg(axis))

  y_axis_specs_arg = []
  for axis in row_axes:
    y_axis_specs_arg.append(axis_spec_arg(axis))

  sliced_axis_specs_arg = []
  for axis in slider_axes:
    sliced_axis_specs_arg.append(axis_spec_arg(axis))

  args_json = json.dumps({
      "info": info,
      "arrayBase64": base64.b64encode(converted_array_data.tobytes()).decode(
          "ascii"
      ),
      "arrayDtype": array_dtype,
      "validMaskBase64": base64.b64encode(
          valid_mask.astype(np.uint8).tobytes()
      ).decode("ascii"),
      "dataStrides": strides,
      "xAxisSpecs": x_axis_specs_arg,
      "yAxisSpecs": y_axis_specs_arg,
      "slicedAxisSpecs": sliced_axis_specs_arg,
      "colormapConfig": {
          "type": cmap_type,
          "min": vmin,
          "max": vmax,
          "dynamic": dynamic_continuous_cmap,
          "rawMinAbs": raw_min_abs,
          "rawMaxAbs": raw_max_abs,
          "cmapData": cmap_data,
      },
      "pixelsPerCell": pixels_per_cell,
      "valueFormattingInstructions": formatting_instructions,
  })
  # Note: We need to save the parent of the treescope-run-here element first,
  # because it will be removed before the runSoon callback executes.
  inner_fn = html_escaping.without_repeated_whitespace("""
    const parent = this.parentNode;
    const defns = this.getRootNode().host.defns;
    defns.runSoon(() => {
        const tpl = parent.querySelector('template.deferred_args');
        const config = JSON.parse(
            tpl.content.querySelector('script').textContent
        );
        tpl.remove();
        defns.arrayviz.buildArrayvizFigure(parent, config);
    });
  """)
  src = (
      '<div class="arrayviz_container">'
      '<span class="loading_message">Rendering array...</span>'
      f'<treescope-run-here><script type="application/octet-stream">{inner_fn}'
      "</script></treescope-run-here>"
      '<template class="deferred_args">'
      f'<script type="application/json">{args_json}</script></template></div>'
  )
  return src

