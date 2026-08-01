
def make_matmul_weight_only_node(
    node,
    weight_shape,
    num_bits,
    group_size,
    k_blocks,
    q_weight,
    scale,
    zero_point,
    accuracy_level=0,
):  # pragma: no cover
    """Build MatMulNBits node.

    Args:
        node: original matmul node
        weight_shape: original weight shape
        num_bits (int): num_bits
        group_size (int): how many elements share one scale/zp
        k_blocks (int): block number
        q_weight (array): quantized weight
        scale (array): scale
        zero_point (array): zero point
        accuracy_level (int): accuracy level. Support 0 (unset), 1(fp32), 2(fp16), 3(bf16), or 4(int8).

    Returns:
        matmul_weight_only_node: MatMulNBits node
        new_inits: initializers of the new node
    """
    blob_size = group_size * num_bits // 8
    packed = np.zeros((q_weight.shape[0], blob_size), dtype="uint8")
    q_weight_name = node.input[1] + f"_Q{num_bits!s}G{group_size!s}"
    input_names = [node.input[0], q_weight_name]
    new_inits = []
    kwargs = {}

    op_type = "MatMulNBits"

    # pack quantized weight
    if num_bits == 4:
        q_weight_pairs = q_weight[:, ::2] | q_weight[:, 1::2] << 4
        packed[:, :] = q_weight_pairs[:, :blob_size]
    elif num_bits == 8:
        packed = q_weight
    else:
        logger.error(f"MatMulNBits does not have kernel support for num_bits = {num_bits}.")

    packed = np.reshape(packed, (-1, k_blocks, blob_size))

    # build scale tensor
    scale = np.reshape(scale, (-1, k_blocks))
    assert scale.dtype == np.float32 or scale.dtype == np.float16
    scale_tensor = onnx.helper.make_tensor(
        name=node.input[1] + "_scale",
        data_type=np_dtype_to_tensor_dtype(scale.dtype),
        dims=scale.shape,
        vals=scale.tobytes(),
        raw=True,
    )
    input_names.append(scale_tensor.name)
    new_inits.append(scale_tensor)

    # build zero_point tensor
    if zero_point is not None:
        if num_bits == 8:
            packed_zp = zero_point.astype("uint8")
        elif num_bits == 4:
            # For 4-bit case, the default zeros is 0x8. So it is 0x88 = 136 if we fill lower/higher 4 bits with 0x8.
            packed_zp = np.full((zero_point.shape[0] + 1) // 2, 136, dtype="uint8")
            # create an index array
            idx = np.arange(zero_point.shape[0] // k_blocks * k_blocks).reshape(-1)
            # separate odd and even indices
            even_idx = idx[::2]
            odd_idx = idx[1::2]
            # vectorized operation for even and odd indices
            packed_zp[even_idx // 2] = (packed_zp[even_idx // 2] & 0xF0) | zero_point[even_idx].ravel()
            packed_zp[odd_idx // 2] = (packed_zp[odd_idx // 2] & 0x0F) | (zero_point[odd_idx].ravel() << 4)
        else:
            raise ValueError(f"MatMulNBits does not have kernel support for num_bits = {num_bits}.")

        packed_zp = np.reshape(packed_zp, (weight_shape[1], -1))
        zp_tensor = onnx.helper.make_tensor(
            name=node.input[1] + "_zp", data_type=2, dims=packed_zp.shape, vals=packed_zp.tobytes(), raw=True
        )
        input_names.append(zp_tensor.name)
        new_inits.append(zp_tensor)

    # set kwargs
    kwargs["K"] = weight_shape[0]
    kwargs["N"] = weight_shape[1]
    kwargs["bits"] = num_bits
    kwargs["block_size"] = group_size
    if accuracy_level > 0:
        # require onnxruntime > 1.16.3
        kwargs["accuracy_level"] = accuracy_level

    q_weight_tensor = onnx.helper.make_tensor(
        name=q_weight_name,
        data_type=2,
        dims=packed.shape,
        vals=packed.tobytes(),
        raw=True,
    )
    new_inits.append(q_weight_tensor)

    matmul_weight_only_node = onnx.helper.make_node(
        op_type,
        inputs=input_names,
        outputs=node.output,
        name=node.name + "_Q" + str(num_bits) if node.name else "_Q" + str(num_bits),
        domain="com.microsoft",
        **kwargs,
    )
    return matmul_weight_only_node, new_inits

