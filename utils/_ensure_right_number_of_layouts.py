from typing import Callable

def _ensure_right_number_of_layouts(
    filter_fn: Callable[[ir.Value], bool],
    attr_suffix: str,
    value_type: str,
    op: ir.OpView,
) -> None:
  """Ensures that the right number of in/out layouts are provided for an op.

  Layouts here are can be vector layouts, TMEM layouts, or SMEM transforms.
  """
  layouts = lambda attr: op.attributes[attr] if attr in op.attributes else []
  in_layouts = layouts(f"in_{attr_suffix}")
  out_layouts = layouts(f"out_{attr_suffix}")

  num_matching_operands = sum(map(filter_fn, op.operands))
  if len(in_layouts) != num_matching_operands:
    raise ValueError(
        f"Expected the same number of in_{attr_suffix} ({len(in_layouts)}) as "
        f"{value_type} operands ({num_matching_operands}). op=\n  {op}"
    )
  num_matching_results = sum(map(filter_fn, op.results))
  if len(out_layouts) != num_matching_results:
    raise ValueError(
        f"Expected the same number of out_{attr_suffix} ({len(out_layouts)}) "
        f"as {value_type} results ({num_matching_results}). op=\n  {op}"
    )

