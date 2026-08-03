import json
from typing import Any

def _lower_pin(ctx, x_op, *, to):
  color = {'vmem': 1, 'hbm': 0, None: None}[to]
  if color is not None:
    backend_config = json.dumps({
        "custom_call_config": {
            "output_memory_space_colors": [
                {
                    "shape_index": [],
                    "color": str(color)
                }
            ]
        }
    })
    config: dict[str, Any] = dict(backend_config=backend_config)
  else:
    config = {}
  out_aval, = ctx.avals_out
  flat_ops, _ = mlir.ir_tree_registry.flatten([x_op])
  flat_res_types, _ = mlir.ir_tree_registry.flatten(mlir.aval_to_ir_types(ctx.module_context, out_aval))
  return mlir.custom_call(
      "Pin",
      operands=flat_ops,
      result_types=flat_res_types,
      **config,
  ).results

