from typing import Any

def is_function(
    value: Any,
) -> TypeIs[_FuncTypes]:
    return isinstance(
        value,
        (
            types.FunctionType,
            types.BuiltinFunctionType,
            types.MethodDescriptorType,
            types.WrapperDescriptorType,
        ),
    )

