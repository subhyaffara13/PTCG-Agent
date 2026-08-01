
def run_candidate(
    task: ParityTask,
    args,
    last_matmul_node_name,
    op_block_list=["FastGelu", "LayerNormalization"],  # noqa: B006
):
    parameters = get_mixed_precision_parameters(args, last_matmul_node_name, op_block_list)
    op_block_list_str = ",".join(sorted(op_block_list))

    if op_block_list:
        name = f"Mixed precision baseline + {op_block_list_str} in FP32"
    else:
        name = f"Mixed precision baseline (logits output and last MatMul node {last_matmul_node_name} in FP32)"

    env_vars = get_ort_environment_variables()
    if env_vars:
        name = name + f" ({env_vars})"

    task.run(parameters, name)

