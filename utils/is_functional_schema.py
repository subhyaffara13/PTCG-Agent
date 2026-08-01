
def is_functional_schema(schema: Any, *, allow_valid_view: bool = False) -> bool:
    """Check if the schema is functional.

    An operator is functional if:
    - it does not mutate any of its inputs
    - If no view are allowed
        - it does not return a view on any of its inputs
    - If valid views are allowed
        - it is not a view or a view with a single input Tensor and single output Tensor
    - it has at least one return
    """

    def is_functional(schema):
        if schema.is_mutable:
            return False
        rets = schema.returns
        is_non_mutating_view = len(rets) > 0 and any(
            r.alias_info is not None and not r.alias_info.is_write for r in rets
        )
        num_tensor_inputs = 0
        num_tensor_outputs = 0

        if isinstance(schema, torch.FunctionSchema):
            for arg in schema.arguments:
                if isinstance(arg.type, torch.TensorType):
                    num_tensor_inputs += 1

            for ret in schema.returns:
                if isinstance(ret.type, torch.TensorType):
                    num_tensor_outputs += 1

        elif isinstance(schema, torchgen.model.FunctionSchema):
            for argument in schema.arguments.flat_non_out:
                if argument.type.is_tensor_like():
                    num_tensor_inputs += 1

            for ret_arg in schema.returns:
                if ret_arg.type.is_tensor_like():
                    num_tensor_outputs += 1

        if is_non_mutating_view:
            return allow_valid_view and (
                num_tensor_inputs == 1 and num_tensor_outputs == 1
            )
        if not schema.returns:
            return False
        return True

    if isinstance(schema, torch._C.FunctionSchema):
        return is_functional(schema)

    # Lazy import because not all PyTorch builds have torchgen
    from torchgen.model import FunctionSchema

    if isinstance(schema, str):
        schema = FunctionSchema.parse(schema)
    if not isinstance(schema, FunctionSchema):
        raise AssertionError(f"schema must be FunctionSchema, got {type(schema)}")
    return is_functional(schema)

