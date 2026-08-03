from typing import Any

def check_user_input_output(flat_values: list[Any], error_type: UserErrorType) -> None:
    supported_types = [
        torch.Tensor,
        torch.SymInt,
        torch.SymFloat,
        torch.SymBool,
        torch._C.ScriptObject,
        _IntWrapper,
    ] + list(common_constant_types)

    def is_supported_type(val: Any) -> bool:
        return isinstance(val, tuple(supported_types)) or is_opaque_type(type(val))

    value_type = "input" if error_type == UserErrorType.INVALID_INPUT else "output"
    # We only check that the outputs are not None. Inputs can be None.
    for v in flat_values:
        if not is_supported_type(v):
            if error_type == UserErrorType.INVALID_INPUT and v is None:
                continue

            raise UserError(
                error_type,
                f"It looks like one of the {value_type}s with type `{type(v)}` "
                "is not supported or pytree-flattenable. \n"
                f"Exported graphs {value_type}s can only contain the "
                f"following supported types: {supported_types}. \n"
                "If you are using a custom class object, "
                "please register a pytree_flatten/unflatten function "
                "using `torch.utils._pytree.register_pytree_node` or "
                "`torch.export.register_dataclass`.",
            )

