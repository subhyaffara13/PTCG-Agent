
def gptq_quantize(
    model,
    dataloader,
    weight_config={},  # noqa: B006
    num_bits=4,
    group_size=32,
    scheme="asym",
    n_samples=128,
    percdamp=0.01,
    blocksize=128,
    actorder=False,
    mse=False,
    perchannel=True,
    accuracy_level=0,
    providers=["CPUExecutionProvider"],  # noqa: B006
):
    """Quant the model with GPTQ method.

    Args:
        model (ModelProto or ONNXModel): onnx model
        dataloader (object): dataloader for calibration.
        weight_config (dict): quantization config
                For example,
                weight_config = {
                    'fc2':
                        {
                            'bits': 4,
                            'group_size': 32,
                            'scheme': 'sym',
                            'algorithm': 'GPTQ'
                        }
                }
        num_bits (int, optional): num_bits. Default is 4.
        group_size (int, optional): how many elements share one scale/zp. Default is 32.
        scheme (str, optional): sym or asym. Defaults to "asym".
        n_samples (int, optional): calibration sample number.
        percdamp (float, optional): percent of the average Hessian diagonal to use for dampening.
        blocksize (int, optional): blocksize to quantize weight.
        actorder (bool, optional): whether rearrange Hessian matrix considering the diag's value.
        mse (bool, optional): whether get scale and zero point with mse error.
        perchannel (bool, optional): whether quantize weight per-channel.
        accuracy_level (int): accuracy level. Support 0 (unset), 1(fp32), 2(fp16), 3(bf16), or 4(int8).
        providers (list): providers to use

    Returns:
        model: fake quantized ONNXModel
    """
    model = ONNXModel(model)
    base_dir = os.path.dirname(model.model_path) if model.model_path is not None else ""

    inputs, so = prepare_inputs(model, n_samples, dataloader, providers)
    del dataloader
    org_output = copy.deepcopy(model.model.graph.output)
    model.remove_tensors_from_outputs([i.name for i in org_output])
    output_names = []
    for node in model.nodes():
        if (
            node.op_type in ["MatMul"]
            and weight_config.get(node.name, {}) != "fp32"
            and weight_config.get(node.name, {}).get("algorithm", "GPTQ") == "GPTQ"
        ):
            output_names.append(node.input[0])
    output_names = list(set(output_names))
    model.add_tensors_to_outputs(output_names)
    if model.is_large_model:
        onnx.save_model(
            model.model,
            model.model_path + "_augment.onnx",
            save_as_external_data=True,
            all_tensors_to_one_file=True,
            convert_attribute=False,
        )

    session = (
        ort.InferenceSession(model.model.SerializeToString(), so, providers=providers)
        if not model.is_large_model
        else ort.InferenceSession(model.model_path + "_augment.onnx", so, providers=providers)
    )

    for idx, input_name in enumerate(output_names):
        simple_progress_bar(len(output_names), idx + 1)
        node_list = []
        weights = []

        for node in model.input_name_to_nodes[input_name]:
            if (
                node.op_type in ["MatMul"]
                and weight_config.get(node.name, {}) != "fp32"
                and weight_config.get(node.name, {}).get("algorithm", "GPTQ") == "GPTQ"
                and model.get_initializer(node.input[1]) is not None
            ):
                weight = numpy_helper.to_array(
                    model.get_initializer(model.get_node(node.name).input[1]), base_dir
                ).copy()
                if len(weight.shape) != 2:
                    continue

                weights.append(weight)
                node_list.append(model.get_node(node.name))

        if len(weights) == 0:
            continue

        Hs = [np.zeros((i.shape[0], i.shape[0])) for i in weights]  # noqa: N806
        nsamples = 0
        for data in inputs:
            inp = session.run([input_name], data)[0]
            tmp = inp.shape[0]
            inp = np.reshape(inp, (-1, inp.shape[-1]))
            Hs = [i * (nsamples / (nsamples + tmp)) for i in Hs]  # noqa: N806
            nsamples += tmp
            inp = np.sqrt(2 / nsamples) * inp
            Hs = [i + np.matmul(inp.T, inp) for i in Hs]  # noqa: N806

        for (
            node,
            weight,
            H,  # noqa: N806
        ) in zip(node_list, weights, Hs, strict=False):
            if node.name in weight_config:
                num_bits = weight_config[node.name]["bits"]
                group_size = weight_config[node.name]["group_size"]
                scheme = weight_config[node.name]["scheme"]
            group_size = group_size if group_size != -1 else weight.shape[0]
            dtype = weight.dtype

            q_weight = gptq(
                weight,
                H,
                num_bits=num_bits,
                group_size=group_size,
                scheme=scheme,
                blocksize=blocksize,
                percdamp=percdamp,
                actorder=actorder,
                mse=mse,
                perchannel=perchannel,
            )

            weight_tensor = model.get_initializer(node.input[1])
            init_share_num = model.get_initializer_share_num(node.input[1])

            satisfy_MatMulNBits_condition = num_bits == 4  # noqa: N806

            if satisfy_MatMulNBits_condition:  # pragma: no cover
                org_shape = weight.shape
                k_blocks = (org_shape[0] + group_size - 1) // group_size
                q_weight = pad_tensor(q_weight, group_size, k_blocks)
                q_weight, scale, zp = quant_tensor(q_weight.T, num_bits, group_size, scheme, "uint")
                q_matmul_node, new_inits = make_matmul_weight_only_node(
                    node=node,
                    weight_shape=org_shape,
                    num_bits=num_bits,
                    group_size=group_size,
                    k_blocks=k_blocks,
                    q_weight=q_weight.astype("uint8"),
                    scale=scale.astype(dtype),
                    zero_point=zp if scheme == "asym" else None,
                    accuracy_level=accuracy_level,
                )

                model.add_initializers(new_inits)
                model.remove_node(node)
                model.add_node(q_matmul_node)
            else:
                q_weight_tensor = onnx.helper.make_tensor(
                    name=node.input[1] + f"_Q{num_bits!s}G{group_size!s}",
                    data_type=np_dtype_to_tensor_dtype(dtype),
                    dims=q_weight.shape,
                    vals=q_weight.astype(dtype).tobytes(),
                    raw=True,
                )
                model.add_initializer(q_weight_tensor)
                node.input[1] = q_weight_tensor.name
            if init_share_num == 1:
                model.remove_initializer(weight_tensor)

    model.remove_tensors_from_outputs(output_names)
    model.model.graph.output.MergeFrom(org_output)

    model.topological_sort()

    # reload external data to prevent external data file path errors
    if model.is_large_model:
        from onnx.external_data_helper import load_external_data_for_model  # noqa: PLC0415

        load_external_data_for_model(model.model, os.path.split(model.model_path)[0])

    return model

