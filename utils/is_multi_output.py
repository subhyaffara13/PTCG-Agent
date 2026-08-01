
def is_multi_output(func: FunctionSchema) -> bool:
    return len(func.returns) > 1 or (
        len(func.returns) == 1 and func.returns[0].type.is_list_like() is not None
    )

