
def _get_output_metadata_by_execution(subgraph, *operands):
    """
    Fallback: Extract metadata by executing the subgraph.
    This should only be used when static analysis fails.
    WARNING: This will run side-effectful operations!
    """

    with suspend_functionalization(), disable_functional_mode():
        with disable_proxy_modes_tracing():
            # args are functional tensors, generate some example tensors
            fw_inputs = pytree.tree_map(_from_fun, operands)

            from torch._guards import detect_fake_mode

            fake_mode = detect_fake_mode(fw_inputs)
            context = (
                nullcontext()
                if fake_mode is None or fake_mode.shape_env is None
                else fake_mode.shape_env.ignore_fresh_unbacked_symbols()
            )

            with context:
                fw_outs = pytree.tree_map(_from_fun, subgraph(*fw_inputs))

            num_fw_outs = len(fw_outs)

            output_metadata = OutputMetadata()
            output_metadata.num_fw_outs = num_fw_outs

            for idx, fw_out in enumerate(fw_outs):
                if isinstance(fw_out, torch.SymInt):
                    output_metadata.indexes_with_symint.add(idx)
                elif not fw_out.requires_grad:
                    output_metadata.indexes_with_no_grad.add(idx)

            return output_metadata

