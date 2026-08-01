
def num_fw_fixed_arguments(dynamo_gm_num_inputs: int, aot_fw_gm_num_inputs: int) -> int:
    "Computes the number of inputs to the aot fw graph which have fixed addresses (params and buffers)"
    num_rng_seed_offset_inputs = (
        2 if torch._functorch.config.functionalize_rng_ops else 0
    )
    # AOT won't lift any parameters if we're inlining NN Modules
    # however desugaring subclasses will still add arguments
    # resulted in extra fixed inputs https://github.com/pytorch/pytorch/issues/130502
    return aot_fw_gm_num_inputs - dynamo_gm_num_inputs - num_rng_seed_offset_inputs

