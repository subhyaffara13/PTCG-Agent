
def rtn_quantize(
    model,
    weight_config={},  # noqa: B006
    num_bits=4,
    group_size=32,
    scheme="asym",
    ratios={},  # noqa: B006
    accuracy_level=0,
    providers=["CPUExecutionProvider"],  # noqa: B006
    algorithm="k_quant",
):
    """Quant the model with round to nearst method.

    Args:
        model (ModelProto or ONNXModel): onnx model
        weight_config (dict): quantization config
                For example,
                weight_config = {
                    'fc2':
                        {
                            'bits': 4,
                            'group_size': 32,
                            'scheme': 'sym',
                            'algorithm': 'RTN'
                        }
                }
        num_bits (int, optional): num_bits. Default is 4.
        group_size (int, optional): how many elements share one scale/zp. Default is 32.
        scheme (str, optional): sym or asym. Defaults to "asym".
        ratios (dict, optional): percentile of clip. Defaults to {}.
        accuracy_level (int): accuracy level. Support 0 (unset),1(fp32), 2(fp16), 3(bf16), or 4(int8).
        providers (list): providers to use

    Returns:
        model: fake quantized ONNXModel
    """
    model = ONNXModel(model)
    base_dir = os.path.dirname(model.model_path) if model.model_path is not None else ""
    new_nodes = []
    remove_nodes = []
    total_num = len([i for i in model.nodes() if i.op_type in ["MatMul"]])
    curr_id = 0
    for node in model.nodes():
        if node.op_type in ["MatMul"]:
            curr_id += 1
            simple_progress_bar(total_num, curr_id)
        if (
            node.op_type in ["MatMul"]
            and model.get_initializer(node.input[1]) is not None
            and weight_config.get(node.name, {}) != "fp32"
        ):
            weight_tensor = model.get_initializer(node.input[1])
            weight = numpy_helper.to_array(weight_tensor, base_dir=base_dir).copy()
            if len(weight.shape) != 2:
                continue

            dtype = weight.dtype

            if node.name in weight_config:
                num_bits = weight_config[node.name]["bits"]
                group_size = weight_config[node.name]["group_size"]
                scheme = weight_config[node.name]["scheme"]

            org_w_shape = weight.shape  # ic, oc
            group_size = group_size if group_size != -1 else org_w_shape[0]

            k_blocks = (org_w_shape[0] - 1) // group_size + 1
            init_share_num = model.get_initializer_share_num(node.input[1])

            weight = pad_tensor(weight, group_size, k_blocks)

            satisfy_MatMulNBits_condition = num_bits == 4 or num_bits == 8  # noqa: N806

            if satisfy_MatMulNBits_condition:  # pragma: no cover
                if algorithm == "k_quant":
                    q_weight, scale, zp = quant_tensor_k_quant_cuda(weight.T, num_bits, group_size)
                else:
                    q_weight, scale, zp = quant_tensor(
                        weight.T, num_bits, group_size, scheme, "uint", ratios.get(node.input[1], 1)
                    )

                q_matmul_node, new_inits = make_matmul_weight_only_node(
                    node=node,
                    weight_shape=org_w_shape,
                    num_bits=num_bits,
                    group_size=group_size,
                    k_blocks=k_blocks,
                    q_weight=q_weight.astype("uint8"),
                    scale=scale.astype(dtype),
                    zero_point=zp if scheme == "asym" or algorithm == "k_quant" else None,
                    accuracy_level=accuracy_level,
                )

                model.add_initializers(new_inits)
                remove_nodes.append(node)
                new_nodes.append(q_matmul_node)
            else:
                q_weight = qdq_tensor(weight.T, num_bits, group_size, scheme, "int", ratios.get(node.input[1], 1))
                q_weight = np.reshape(q_weight, (org_w_shape[1], -1))
                q_weight = np.transpose(q_weight)
                q_weight = q_weight[: org_w_shape[0], :].astype(dtype)
                q_weight_tensor = onnx.helper.make_tensor(
                    name=node.input[1] + f"_Q{num_bits!s}G{group_size!s}",
                    data_type=np_dtype_to_tensor_dtype(dtype),
                    dims=weight.shape,
                    vals=q_weight.tobytes(),
                    raw=True,
                )
                model.add_initializer(q_weight_tensor)
                node.input[1] = q_weight_tensor.name
            if init_share_num == 1:
                model.remove_initializer(weight_tensor)

    model.add_nodes(new_nodes)
    model.remove_nodes(remove_nodes)
    model.topological_sort()
    return model

