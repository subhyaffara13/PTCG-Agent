
def op_arguments(func: FunctionSchema, is_reverse: bool) -> list[Binding]:
    args = func.arguments.flat_all
    if args[0].type != BaseType(BaseTy.Tensor):
        raise AssertionError(f"Expected first arg to be Tensor, got {args[0].type}")
    non_self_args = args[1:]
    # The forward lambda calls the at::_ops API, while the reverse lambda calls the view inverse API.
    # Both of these follow the dispatcher API.
    non_self_bindings = [dispatcher.argument(a) for a in non_self_args]
    if not is_reverse:
        # the forward lambda swaps out the original tensor argument with the lambd arg "base"
        return [base_binding] + non_self_bindings
    else:
        # the reverse lambda does the same, but with an additional "mutated_view" arg
        # additionally, we have a calling convention: for view ops that return multiple tensor outputs
        # their corresponding view_inverse function takes in an additional index argument.
        if is_multi_output(func):
            return [
                base_binding,
                mutated_view_binding,
                inverse_return_mode_binding,
                out_index_binding,
            ] + non_self_bindings
        else:
            return [
                base_binding,
                mutated_view_binding,
                inverse_return_mode_binding,
            ] + non_self_bindings

