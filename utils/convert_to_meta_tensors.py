
def convert_to_meta_tensors(sig: DispatcherSignature) -> tuple[str, list[Binding]]:
    context: list[Binding] = []
    unwrapped_tensor_args: list[str] = []
    for arg in sig.arguments():
        if is_tensor_like(arg.argument):
            # for tensor inputs, we want to unwrap them before passing them into the redispatch calls.
            a_ = arg.name
            unwrapped_name = f"{arg.name}_meta"
            unwrapped_tensor_args.append(f"auto {unwrapped_name} = to_meta({a_});")
            context.append(arg.with_name(unwrapped_name))
        else:
            # for non-tensor inputs, we want to pass them directly into the redispatch calls.
            context.append(arg)
    unwrap_tensor_args_str = "\n        ".join(unwrapped_tensor_args)
    return unwrap_tensor_args_str, context


def convert_to_meta_tensors(sig: DispatcherSignature) -> tuple[str, list[Binding]]:
    context: list[Binding] = []
    unwrapped_tensor_args: list[str] = []
    for arg in sig.arguments():
        if isinstance(arg.argument, Argument) and arg.argument.type.is_tensor_like():
            unwrapped_name = f"{arg.name}_meta"
            unwrapped_tensor_args.append(
                f"auto {unwrapped_name} = to_meta({arg.name});"
            )
            context.append(arg.with_name(unwrapped_name))
        else:
            context.append(arg)
    unwrap_tensor_args_str = "\n        ".join(unwrapped_tensor_args)
    return unwrap_tensor_args_str, context

