from typing import Any

def _maybe_unlift_partitioned_effect_tokens(
    fw_module: torch.fx.GraphModule,
    bw_module: torch.fx.GraphModule,
    joint_inputs: list[Any] | tuple[list[Any], list[Any]],
    fw_metadata: ViewAndMutationMeta,
    aot_config: AOTConfig,
    num_inner_fwd_outputs: int,
) -> tuple[int, list[Any] | tuple[list[Any], list[Any]]]:
    num_tokens = len(fw_metadata.tokens)

    # See Note [Side-Effectful Tokens in AOTAutograd]
    if config.unlift_effect_tokens and (
        num_tokens > 0 or fw_metadata.num_backward_tokens > 0
    ):
        unlift_tokens(fw_module, fw_metadata, aot_config, bw_module)
        num_inner_fwd_outputs -= num_tokens
        if isinstance(joint_inputs, tuple):
            joint_inputs = (
                _joint_inputs_for_forward(joint_inputs)[num_tokens:],
                joint_inputs[1],
            )
        else:
            joint_inputs = joint_inputs[num_tokens:]

    return num_inner_fwd_outputs, joint_inputs

