
def get_fn_code(fn_var: Any) -> types.CodeType | None:
    if isinstance(fn_var, UserFunctionVariable):
        return fn_var.get_function().__code__
    elif isinstance(fn_var, UnspecializedNNModuleVariable):
        return (
            fn_var.value.forward.__func__.__code__  # pyrefly: ignore[missing-attribute]
        )
    return None

