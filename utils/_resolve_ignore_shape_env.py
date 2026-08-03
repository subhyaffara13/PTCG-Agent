from typing import Any

def _resolve_ignore_shape_env(dynamic_shapes: Any):
    # tells compile_fx to ignore the shape_envs on the ambient context
    # and the graph_module.
    return dynamic_shapes == "from_example_inputs"

