
def find_bert_inputs(
    onnx_model: OnnxModel,
    input_ids_name: str | None = None,
    segment_ids_name: str | None = None,
    input_mask_name: str | None = None,
) -> tuple[np.ndarray | None, np.ndarray | None, np.ndarray | None]:
    """Find graph inputs for BERT model.
    First, we will deduce inputs from EmbedLayerNormalization node.
    If not found, we will guess the meaning of graph inputs based on naming.

    Args:
        onnx_model (OnnxModel): onnx model object
        input_ids_name (str, optional): Name of graph input for input IDs. Defaults to None.
        segment_ids_name (str, optional): Name of graph input for segment IDs. Defaults to None.
        input_mask_name (str, optional): Name of graph input for attention mask. Defaults to None.

    Raises:
        ValueError: Graph does not have input named of input_ids_name or segment_ids_name or input_mask_name
        ValueError: Expected graph input number does not match with specified input_ids_name, segment_ids_name
                    and input_mask_name

    Returns:
        Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]: input tensors of input_ids,
                                                                                 segment_ids and input_mask
    """

    graph_inputs = onnx_model.get_graph_inputs_excluding_initializers()

    if input_ids_name is not None:
        input_ids = onnx_model.find_graph_input(input_ids_name)
        if input_ids is None:
            raise ValueError(f"Graph does not have input named {input_ids_name}")

        segment_ids = None
        if segment_ids_name:
            segment_ids = onnx_model.find_graph_input(segment_ids_name)
            if segment_ids is None:
                raise ValueError(f"Graph does not have input named {segment_ids_name}")

        input_mask = None
        if input_mask_name:
            input_mask = onnx_model.find_graph_input(input_mask_name)
            if input_mask is None:
                raise ValueError(f"Graph does not have input named {input_mask_name}")

        expected_inputs = 1 + (1 if segment_ids else 0) + (1 if input_mask else 0)
        if len(graph_inputs) != expected_inputs:
            raise ValueError(f"Expect the graph to have {expected_inputs} inputs. Got {len(graph_inputs)}")

        return input_ids, segment_ids, input_mask

    if len(graph_inputs) != 3:
        raise ValueError(f"Expect the graph to have 3 inputs. Got {len(graph_inputs)}")

    embed_nodes = onnx_model.get_nodes_by_op_type("EmbedLayerNormalization")
    if len(embed_nodes) == 1:
        embed_node = embed_nodes[0]
        input_ids = get_graph_input_from_embed_node(onnx_model, embed_node, 0)
        segment_ids = get_graph_input_from_embed_node(onnx_model, embed_node, 1)
        input_mask = get_graph_input_from_embed_node(onnx_model, embed_node, 7)

        if input_mask is None:
            for input in graph_inputs:
                input_name_lower = input.name.lower()
                if "mask" in input_name_lower:
                    input_mask = input
        if input_mask is None:
            raise ValueError("Failed to find attention mask input")

        return input_ids, segment_ids, input_mask

    # Try guess the inputs based on naming.
    input_ids = None
    segment_ids = None
    input_mask = None
    for input in graph_inputs:
        input_name_lower = input.name.lower()
        if "mask" in input_name_lower:  # matches input with name like "attention_mask" or "input_mask"
            input_mask = input
        elif (
            "token" in input_name_lower or "segment" in input_name_lower
        ):  # matches input with name like "segment_ids" or "token_type_ids"
            segment_ids = input
        else:
            input_ids = input

    if input_ids and segment_ids and input_mask:
        return input_ids, segment_ids, input_mask

    raise ValueError("Fail to assign 3 inputs. You might try rename the graph inputs.")

