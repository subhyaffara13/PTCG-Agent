
def get_fallback_op_name(func: NativeFunction) -> str:
    return (
        f"{func.namespace}.{func.func.name.name}.{func.func.name.overload_name}"
        if func.func.name.overload_name
        else f"{func.namespace}.{func.func.name.name}.default"
    )

