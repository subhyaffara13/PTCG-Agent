
def generate_single_level_function(
    interpreter: FuncTorchInterpreter,
    autograd_function: type[torch.autograd.Function],
) -> type[torch.autograd.function._SingleLevelFunction]:
    level = interpreter.level()

    def forward(*operands: Any) -> Any:
        unwrapped_operands = pytree.tree_map_only(
            torch.Tensor, lambda x: _unwrap_for_grad(x, level), operands
        )
        # Both enable_grad() and _set_fwd_grad_enabled() are necessary no matter
        # the transform. _SingleLevelFunction will turn off both fwd and bwd
        # gradient computation and we need to turn it back on here.
        with torch.enable_grad(), _set_fwd_grad_enabled(True), interpreter.lower():
            unwrapped_output = custom_function_call(
                autograd_function, *unwrapped_operands
            )

        # See NOTE [mark_dirty object identity check]
        def wrap_fn(output: torch.Tensor) -> torch.Tensor:
            return _wrap_for_grad(output, level)

        return wrap_outputs_maintaining_identity(
            unwrapped_output, unwrapped_operands, operands, wrap_fn
        )

    def setup_context(ctx: Any, inputs: Any, output: Any) -> Any:
        return autograd_function.setup_context(ctx, inputs, output)

    # backward is only used if the transform is TransformType.Grad
    def backward(ctx: Any, *grads: Any) -> Any:
        result = autograd_function.backward(ctx, *grads)
        return result

    # jvp is only used if the transform is TransformType.Jvp
    def jvp(ctx: Any, *tangents: Any) -> Any:
        result = autograd_function.jvp(ctx, *tangents)
        return result

    # This is the sequence of magic words to dynamically generate a Subclass with
    # a given name. A Tensor's .grad_fn field has a class name that is the original
    # autograd.Function's name + Backward, so we do this to generate some
    # meaningful name.
    name = f"{autograd_function.__name__}Generated"
    Generated = type(
        name,
        (torch.autograd.function._SingleLevelFunction,),
        {
            "forward": staticmethod(forward),
            "backward": staticmethod(backward),
            "jvp": staticmethod(jvp),
            "setup_context": staticmethod(setup_context),
        },
    )
    return Generated

