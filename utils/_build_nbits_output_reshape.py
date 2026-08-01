
def _build_nbits_output_reshape(
    a_input_name: str,
    b_original_shape: tuple,
    target_graph: GraphProto,
    name_prefix: str,
    pre_reshape_output: str,
    final_output: str,
) -> list[NodeProto]:
    """Build the reshape chain that restores the ONNX MatMul-broadcast output shape.

    MatMulNBits produces shape ``[...A_batch_dims, M, N]`` (rank = rank(A)). To match
    the original ``MatMul(A, B_orig)`` output, where B_orig has all-unit leading
    dims, we need:

        a_rank_eff = max(rank(A), 2)   # ONNX promotes 1-D A to rank-2
        out_shape = [1] * max(rank(B_orig) - a_rank_eff, 0) + A.shape[:-1] + [N]

    This is built dynamically via Shape/Gather/Max/Sub/Max/ConstantOfShape/Slice/Concat
    so it works regardless of A's static rank (handles rank(A) == 1, rank(A) == 2
    — the common transformer case — as well as rank(A) >= rank(B_orig) where no
    leading-1 prepending is needed). All ops used are valid from opset 11 onward.

    Args:
        a_input_name: name of the activation input edge (A) feeding MatMulNBits.
        b_original_shape: the original (pre-squeeze) shape of B, e.g. ``(1, K, N)``.
        target_graph: graph proto to append helper initializers into.
        name_prefix: unique prefix for generated node/initializer names.
        pre_reshape_output: name of the MatMulNBits output edge (the input of the
            generated Reshape).
        final_output: name of the final edge produced by the generated Reshape
            (must match the original MatMul output edge).

    Returns:
        List of nodes to append to the consumer's ``output_nodes`` after the
        MatMulNBits node. Initializers are appended to ``target_graph`` in place.
    """
    rank_b_orig = len(b_original_shape)
    n_dim = b_original_shape[-1]

    # Incorporate the unique output tensor name so initializer names are unique
    # even when multiple MatMul nodes share the same node.name (Fix 2).
    p = name_prefix + "_" + final_output
    init_zero = p + "_zero"
    init_one = p + "_one"
    init_two = p + "_two"
    init_one_vec = p + "_one_vec"
    init_rank_b = p + "_rank_b"
    init_n_vec = p + "_n_vec"
    init_zero_vec = p + "_zero_vec"
    init_one_value_template = p + "_one_value"

    target_graph.initializer.extend(
        [
            onnx.numpy_helper.from_array(np.array(0, dtype=np.int64), name=init_zero),
            onnx.numpy_helper.from_array(np.array(1, dtype=np.int64), name=init_one),
            onnx.numpy_helper.from_array(np.array(2, dtype=np.int64), name=init_two),
            onnx.numpy_helper.from_array(np.array([1], dtype=np.int64), name=init_one_vec),
            onnx.numpy_helper.from_array(np.array(rank_b_orig, dtype=np.int64), name=init_rank_b),
            onnx.numpy_helper.from_array(np.array([n_dim], dtype=np.int64), name=init_n_vec),
            onnx.numpy_helper.from_array(np.array([0], dtype=np.int64), name=init_zero_vec),
        ]
    )

    a_shape = p + "_a_shape"
    a_shape_of_shape = p + "_a_shape_of_shape"
    a_rank = p + "_a_rank"
    a_rank_eff = p + "_a_rank_eff"
    extra_raw = p + "_extra_raw"
    extra_count = p + "_extra_count"
    extra_count_vec = p + "_extra_count_vec"
    extra_ones = p + "_extra_ones"
    a_rank_minus_one = p + "_a_rank_m1"
    a_rank_minus_one_vec = p + "_a_rank_m1_vec"
    a_prefix_shape = p + "_a_prefix_shape"
    target_shape = p + "_target_shape"

    nodes = [
        onnx.helper.make_node("Shape", [a_input_name], [a_shape], name=p + "_shape_a"),
        # Use Shape(shape) + Gather instead of Size to stay within opset 11
        # (Size requires opset >= 13 when applied to a shape tensor).
        # Shape applied to the 1-D shape vector yields [rank_a] as a 1-element
        # tensor; Gather with scalar index 0 extracts it as a scalar int64.
        onnx.helper.make_node("Shape", [a_shape], [a_shape_of_shape], name=p + "_shape_of_a_shape"),
        onnx.helper.make_node("Gather", [a_shape_of_shape, init_zero], [a_rank], name=p + "_gather_rank"),
        # ONNX MatMul promotes a 1-D activation to rank-2 before computing the
        # output shape, so use Max(a_rank, 2) as the effective rank when
        # computing how many leading 1s to prepend.
        onnx.helper.make_node("Max", [a_rank, init_two], [a_rank_eff], name=p + "_max_rank_eff"),
        onnx.helper.make_node("Sub", [init_rank_b, a_rank_eff], [extra_raw], name=p + "_sub"),
        onnx.helper.make_node("Max", [extra_raw, init_zero], [extra_count], name=p + "_max"),
        onnx.helper.make_node("Reshape", [extra_count, init_one_vec], [extra_count_vec], name=p + "_reshape_extra"),
        onnx.helper.make_node(
            "ConstantOfShape",
            [extra_count_vec],
            [extra_ones],
            name=p + "_const_ones",
            value=onnx.helper.make_tensor(
                name=init_one_value_template,
                data_type=TensorProto.INT64,
                dims=[1],
                vals=[1],
            ),
        ),
        onnx.helper.make_node("Sub", [a_rank, init_one], [a_rank_minus_one], name=p + "_sub_one"),
        onnx.helper.make_node(
            "Reshape", [a_rank_minus_one, init_one_vec], [a_rank_minus_one_vec], name=p + "_reshape_rank_m1"
        ),
        onnx.helper.make_node(
            "Slice",
            [a_shape, init_zero_vec, a_rank_minus_one_vec, init_zero_vec],
            [a_prefix_shape],
            name=p + "_slice_a_prefix",
        ),
        onnx.helper.make_node(
            "Concat",
            [extra_ones, a_prefix_shape, init_n_vec],
            [target_shape],
            name=p + "_concat_target",
            axis=0,
        ),
        onnx.helper.make_node(
            "Reshape",
            [pre_reshape_output, target_shape],
            [final_output],
            name=p + "_reshape_out",
        ),
    ]
    return nodes

