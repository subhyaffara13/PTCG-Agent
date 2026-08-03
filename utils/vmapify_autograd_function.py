from typing import Any

def vmapify_autograd_function(
    autograd_function: type[torch.autograd.Function],
    in_dims: Any,
    batch_size: int,
    randomness: str,
) -> type[torch.autograd.Function]:
    def forward(*operands: Any) -> Any:
        outputs, out_dims = restore_vmap(
            autograd_function.forward, in_dims, batch_size, randomness
        )(*operands)
        if isinstance(outputs, torch.Tensor):
            return outputs, out_dims
        else:
            return *outputs, out_dims

    def setup_context(ctx: Any, inputs: Any, outputs: Any) -> None:
        outputs, out_dims = unpack_outputs(outputs)
        key = id(Generated)

        def inner(inputs: Any, outputs: Any) -> None:
            # wrapped_ctx.save_for_backward will:
            # - unwrap batchedtensors into (tensor, bdim)
            # - save_for_backward(*unwrapped_tensors)
            # - assign the bdims to wrapped_ctx._pt_saved_tensors_bdims
            wrapped_ctx = CtxCustomSave(ctx, current_level())
            autograd_function.setup_context(wrapped_ctx, inputs, outputs)

            # input_shapes are used for reductify later to reduce expanded gradients
            # to the correct shape.
            # See NOTE: [Why can't we rely on autograd to reduce expanded gradients?]
            # for more details
            input_shapes = tuple(
                inp.shape if isinstance(inp, torch.Tensor) else None for inp in inputs
            )
            if not hasattr(ctx, "_pt_input_shapes"):
                # pyrefly: ignore [implicit-any]
                ctx._pt_input_shapes = {}
            ctx._pt_input_shapes.update({key: input_shapes})

            if not hasattr(ctx, "_pt_saved_tensors_bdims_stack"):
                # pyrefly: ignore [implicit-any]
                ctx._pt_saved_tensors_bdims_stack = {}
            ctx._pt_saved_tensors_bdims_stack.update(
                {key: (wrapped_ctx._pt_saved_tensors_bdims)}
            )

        # See NOTE: [Why do we need to run setup_context under a vmap?]
        restore_vmap(
            inner,
            (in_dims, out_dims),
            batch_size,
            randomness,
        )(inputs, outputs)

        if not hasattr(ctx, "_pt_out_dims"):
            # pyrefly: ignore [implicit-any]
            ctx._pt_out_dims = {}
        ctx._pt_out_dims.update({key: out_dims})

    def jvp(ctx: Any, *tangents: Any) -> Any:
        key = id(Generated)

        def jvp_no_context(saved_tensors: Any, tangents: Any) -> Any:
            wrapped_ctx = CtxWithSavedTensors(ctx, saved_tensors)
            return autograd_function.jvp(wrapped_ctx, *tangents)

        tangent_in_dims = get_tangents_in_dims(in_dims, tangents)
        out_tangents, out_tangents_dims = restore_vmap(
            jvp_no_context,
            (ctx._pt_saved_tensors_bdims_stack[key], tangent_in_dims),
            batch_size,
            randomness,
        )(ctx.saved_tensors, tangents)

        result = reductify(
            out_tangents, out_tangents_dims, ctx._pt_out_dims[key], batch_size
        )
        if isinstance(result, torch.Tensor):
            return result, None
        else:
            return *result, None

    def backward(ctx: Any, *grad_outputs: Any) -> Any:
        key = id(Generated)
        grad_outputs_ = grad_outputs[:-1]
        grad_outputs_in_dims = ctx._pt_out_dims[key]

        if not isinstance(grad_outputs_in_dims, tuple):
            grad_outputs_in_dims = (grad_outputs_in_dims,)

        grad_outputs_in_dims = tuple(
            in_dim if grad_output is not None else None
            for grad_output, in_dim in zip(grad_outputs_, grad_outputs_in_dims)
        )

        def backward_no_context(inputs: Any) -> Any:
            saved_tensors, grad_outputs = inputs
            wrapped_ctx = CtxWithSavedTensors(ctx, saved_tensors)
            return autograd_function.backward(wrapped_ctx, *grad_outputs)

        grad_ins, grad_ins_dims = restore_vmap(
            backward_no_context,
            ((ctx._pt_saved_tensors_bdims_stack[key], grad_outputs_in_dims),),
            batch_size,
            randomness,
        )((ctx.saved_tensors, grad_outputs_))
        result = reductify(
            grad_ins, grad_ins_dims, in_dims, batch_size, ctx._pt_input_shapes[key]
        )
        return result

    name = f"Vmapped{autograd_function.__name__}"
    Generated = type(
        name,
        (torch.autograd.Function,),
        {
            "forward": staticmethod(forward),
            "backward": staticmethod(backward),
            "jvp": staticmethod(jvp),
            "setup_context": staticmethod(setup_context),
            "generate_vmap_rule": True,
        },
    )

    return Generated

