
def generate_test_value_names(schema: FunctionSchema, index: int) -> str:
    if schema.is_out_fn():
        raise AssertionError(f"Expected non-out function, got {schema}")
    return ",".join(f"{arg.name}{index}" for arg in schema.schema_order_arguments())

