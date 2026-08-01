
def get_mixed_precision_parameters(args, last_matmul_node_name, op_block_list):
    model = args.model_name_or_path
    parameters = f"-m {model} -o --use_gpu -p fp16".split()
    if args.use_external_data_format:
        parameters.append("--use_external_data_format")
    parameters += [
        "--io_block_list",
        "logits",
        "--node_block_list",
        last_matmul_node_name,
    ]

    if op_block_list:
        parameters.extend(["--op_block_list", *op_block_list])

    return parameters

