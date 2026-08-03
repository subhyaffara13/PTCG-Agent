from typing import Any

def _get_num_tensor_inputs(op_schema: OpSchema) -> int:
    num_inputs = 0

    def _count(obj: Any) -> int:
        if isinstance(obj, OpStrategy):
            return 1
        elif isinstance(obj, TupleStrategy):
            return sum(1 for child in obj.children if child is not None)
        elif isinstance(obj, (list, tuple)):
            return sum(_count(child) for child in obj)
        return 0

    for obj in op_schema.args_schema:
        num_inputs += _count(obj)
    # Also count tensor kwargs (e.g., "out" for out-variant ops)
    for obj in op_schema.kwargs_schema.values():
        num_inputs += _count(obj)
    return num_inputs

