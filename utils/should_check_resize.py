
def should_check_resize(schema: FunctionSchema) -> bool:
    schema_str = str(schema)
    type_variant_op_name = schema_str[: schema_str.find("(")]
    return type_variant_op_name not in no_memory_resize_ops

