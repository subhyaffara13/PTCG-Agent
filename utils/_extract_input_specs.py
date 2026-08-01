
def _extract_input_specs(op_schema: OpSchema) -> tuple[DTensorSpec | object, ...]:
    return op_schema.args_schema + tuple(op_schema.kwargs_schema.values())

