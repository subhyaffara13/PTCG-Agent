
def mutated_args_kwargs(schema: _C.FunctionSchema) -> tuple[list[int], list[str]]:
    idxs = []
    keys = []
    for i, info in enumerate(schema.arguments):
        if info.alias_info is not None and info.alias_info.is_write:
            if info.kwarg_only:
                keys.append(info.name)
            else:
                idxs.append(i)
    return idxs, keys

