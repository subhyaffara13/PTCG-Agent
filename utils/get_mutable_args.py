
def get_mutable_args(op: OpOverload) -> tuple[list[str], list[torch.Type]]:
    return get_mutable_args_from_schema(op._schema)

