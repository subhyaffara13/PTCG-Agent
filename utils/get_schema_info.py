
def get_schema_info(func: OpOverload) -> torch._C._SchemaInfo:
    return torch._C._SchemaInfo(func._schema)

