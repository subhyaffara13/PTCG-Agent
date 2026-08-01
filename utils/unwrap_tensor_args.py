
def unwrap_tensor_args(
    sig: DispatcherSignature, *, is_view_op: bool
) -> tuple[str, list[Binding]]:
    context: list[Binding] = []
    unwrapped_tensor_args: list[str] = []
    for arg in sig.arguments():
        if is_tensor_like(arg.argument):
            # for tensor inputs, we want to unwrap them before passing them into the redispatch calls.
            unwrapped_name = f"{arg.name}_"
            # For most ops, the functionalization needs to sync any pending updates on the input tensors
            # before calling the operator, since otherwise the operator will act on stale data.
            # For view ops though, we can continue to defer syncing until the tensor is used by
            # a non-view operator.
            maybe_sync_input = (
                "" if is_view_op else f"at::functionalization::impl::sync({arg.name});"
            )
            unwrapped_type, conversion_fn = get_owning_type(
                arg.nctype.remove_const_ref().type
            )
            unwrapped_tensor_args.append(
                f"""
      {unwrapped_type.cpp_type()} {unwrapped_name};
      if (at::functionalization::impl::isFunctionalTensor({arg.name})) {{
        {maybe_sync_input}
        {unwrapped_name} = at::functionalization::impl::from_functional_tensor({arg.name});
      }} else {{
        {unwrapped_name} = {conversion_fn(arg.name)};
      }}"""
            )
            context.append(arg.with_name(unwrapped_name))
        else:
            # for non-tensor inputs, we want to pass them directly into the redispatch calls.
            context.append(arg)
    unwrap_tensor_args_str = "\n      ".join(unwrapped_tensor_args)
    return unwrap_tensor_args_str, context

