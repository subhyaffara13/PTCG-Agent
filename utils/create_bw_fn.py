
def create_bw_fn(
    fn: Callable, args: tuple[Any, ...], return_fw_outputs: bool = False
) -> Callable:
    """
    For a fn that accepts flat inputs and returns flat outputs:
        fw_out = fn(*args),
    this function returns:
        grad_args = bw_fn(*args_and_grad_output)
    with the following invariants:
      1. args + fw_out has an 1-1 correspondence to args_and_grad_output
      2. grad_args has an 1-1 corresponsence to args
      3. for tensor arg whose requires_grad is False, its corresponding grad in
         grad_args will be a zero tensor with the same shape.
    """

    from torch._functorch.aot_autograd import AOTConfig, create_joint

    # pyrefly: ignore [missing-module-attribute]
    from torch._higher_order_ops.utils import prepare_fw_with_masks_all_requires_grad

    dummy_aot_config = AOTConfig(
        fw_compiler=None,  # type: ignore[arg-type]
        bw_compiler=None,  # type: ignore[arg-type]
        partition_fn=None,  # type: ignore[arg-type]
        decompositions={},
        num_params_buffers=0,
        aot_id=0,
        keep_inference_input_mutations=False,
    )
    n_primals = len(args)

    bw_fn = create_joint(
        prepare_fw_with_masks_all_requires_grad(fn), aot_config=dummy_aot_config
    )

    def flat_fn(*args_and_grad_outs):
        primals = args_and_grad_outs[:n_primals]
        tangents = args_and_grad_outs[n_primals:]
        fw_outs, grad_args = bw_fn(primals, tangents)
        if len(args) != len(grad_args):
            raise AssertionError(
                f"Expected {len(args)} grad_args, got {len(grad_args)}"
            )

        # For tensors whose grad is None, create zero tensors as gradients
        # This invariant is useful for cudagraph.
        grad_args = [
            torch.zeros_like(arg)
            if isinstance(arg, torch.Tensor) and grad is None
            else grad
            for grad, arg in zip(grad_args, primals)
        ]

        final_grads = _clone_aliasing_output(args_and_grad_outs, grad_args)
        if return_fw_outputs:
            return *fw_outs, *final_grads
        return final_grads

    return flat_fn

