
def stage_backward(
    stage_output,
    output_grads,
    input_values,
    outputs_with_grads_idxs: list[int] | None = None,  # deprecated, not used
) -> tuple[torch.Tensor | None, ...]:
    """
    This is a helper function to:
    1. compute the gradients for the stage inputs, and
    2. accumulate gradients for the stage module's parameters.

    Given the input value(s) and the corresponding gradient for the output
    value(s), compute and accumulate gradients for all parameter values (leaves
    in the autograd trace) as well as return a list of the gradients for the
    input values
    """
    if outputs_with_grads_idxs is not None:
        # Deprecated, not used in runtime calls, only exists in compiler
        stage_output = [stage_output[i] for i in outputs_with_grads_idxs]
        output_grads = [output_grads[i] for i in outputs_with_grads_idxs]

    try:
        # stage_output may be a composite datatype like dict. Extract all individual
        # tensor values here
        stage_output_tensors: list[torch.Tensor] = []
        output_grad_tensors: list[torch.Tensor | None] = []

        def extract_tensors_with_grads(
            output_val,
            grad_val,
            # Don't delete me- see [Note: ref cycle]
            extract_tensors_with_grads,
        ):
            if isinstance(output_val, torch.Tensor):
                if not output_val.requires_grad and output_val.grad_fn is None:
                    return
                if not isinstance(grad_val, (torch.Tensor, type(None))):
                    raise AssertionError(
                        f"Expected Tensor or None gradient but got {type(grad_val)}"
                    )
                stage_output_tensors.append(output_val)
                output_grad_tensors.append(grad_val)
            elif isinstance(output_val, (tuple, list)):
                if grad_val is None:
                    return
                if not isinstance(grad_val, (tuple, list)):
                    raise AssertionError(
                        f"grad_value expected to have type {type(output_val)} but got {type(grad_val)}"
                    )
                if not len(output_val) == len(grad_val):
                    raise AssertionError(
                        f"Expected len(output_val) == len(grad_val), got {len(output_val)} != {len(grad_val)}"
                    )
                for ov, gv in zip(output_val, grad_val):
                    extract_tensors_with_grads(
                        ov,
                        gv,
                        extract_tensors_with_grads,
                    )
            elif isinstance(output_val, dict):
                if grad_val is None:
                    return
                if not isinstance(grad_val, dict):
                    raise AssertionError(f"Expected dict, got {type(grad_val)}")
                if not set(output_val.keys()) == set(grad_val.keys()):
                    raise AssertionError(
                        f"Expected keys {set(output_val.keys())}, got {set(grad_val.keys())}"
                    )
                for k in output_val:
                    extract_tensors_with_grads(
                        output_val[k], grad_val[k], extract_tensors_with_grads
                    )
            else:
                # Output is a non-tensor type; just ignore it
                pass

        # Note: ref cycle
        # break a ref cycle that would keep tensors alive until GC runs
        # 1. extract_tensors_with_grads refers to a cell that holds refs to any vars defined in stage_backward
        #    and used in extract_tensors_with_grads
        # 2. extract_tensors_with_grads referred to both stage_output_tensors, output_grad_tensors,
        #    and to itself (extract_tensors_with_grads) since it makes a recursive call
        # 3. stage_output_tensors was kept alive by the above refcycle, and it holds activation tensors, which is bad
        # fix -> explicitly pass in the ref to the fn, so there is no gc cycle anymore
        extract_tensors_with_grads(
            stage_output, output_grads, extract_tensors_with_grads
        )

        torch.autograd.backward(
            stage_output_tensors,
            grad_tensors=output_grad_tensors,  # type: ignore[arg-type]
        )

        # Extract gradients wrt the input values
        grad_inputs: list[torch.Tensor | None] = []
        for val in input_values:
            if isinstance(val, torch.Tensor):
                grad_inputs.append(val.grad)
                # Since gradients that will pass back to previous stages do not require gradient accumulation,
                # by decrementing the gradients' reference count at this point, the memory of gradients will be
                # returned to the allocator as soon as the next micro batch's get_bwd_send_ops comes and current
                # asynchronous send completes.
                # This prevents the gradients from persisting in GPU memory for the entire duration of step_microbatches
                # until clear_runtime_states() is called.
                val.grad = None
            else:
                grad_inputs.append(None)

        # Alternative impl: `torch.autograd.grad`.
        # Note that `torch.autograd.grad` will not accumulate gradients into the
        # model's parameters.
        """
        inputs_with_grad = []
        for val in input_values:
            if isinstance(val, torch.Tensor) and val.requires_grad:
                inputs_with_grad.append(val)

        grad_inputs = torch.autograd.grad(
            stage_output_tensors, inputs_with_grad, output_grad_tensors,  # type: ignore[arg-type]
        )
        """

    except Exception as e:
        exc_msg = f"""
        Failed to run stage backward:
        Stage output: {map_debug_info(stage_output)}
        Output gradient: {map_debug_info(output_grads)}
        Input: {map_debug_info(input_values)}
        """
        raise RuntimeError(exc_msg) from e

    return tuple(grad_inputs)

