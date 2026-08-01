
def export_longformer(model: LongformerModel, onnx_model_path: str, export_padding: bool):
    """Export longformer model to ONNX

    Args:
        model (LongformerModel): longformer model
        onnx_model_path (str): output onnx path
        export_padding (bool): whether export padding logic to ONNX so that input string can be any length.

    Raises:
        RuntimeError: This tool requires transformers 4.0.0 or later.
        RuntimeError: LongformerSelfAttention.forward arguments are different.
    """
    input_ids, attention_mask, global_attention_mask = get_dummy_inputs(
        model.config, export_padding, device=torch.device("cpu")
    )

    _ = model(
        input_ids,
        attention_mask=attention_mask,
        global_attention_mask=global_attention_mask,
    )

    if version.parse(transformers.__version__) < version.parse("4.0.0"):
        raise RuntimeError("This tool requires transformers 4.0.0 or later.")

    # Here we replace LongformerSelfAttention.forward using our implementation for exporting ONNX model
    key = " ".join(inspect.getfullargspec(LongformerSelfAttention.forward).args)
    args_to_func = {
        "self hidden_states attention_mask layer_head_mask is_index_masked is_index_global_attn is_global_attn output_attentions": my_longformer_self_attention_forward_4_3_2,
        "self hidden_states attention_mask is_index_masked is_index_global_attn is_global_attn output_attentions": my_longformer_self_attention_forward_4_3,
        "self hidden_states attention_mask is_index_masked is_index_global_attn is_global_attn": my_longformer_self_attention_forward_4,
    }

    if key not in args_to_func:
        print(
            "Current arguments",
            inspect.getfullargspec(LongformerSelfAttention.forward).args,
        )
        raise RuntimeError(
            "LongformerSelfAttention.forward arguments are different. Please install supported version (like transformers 4.3.0)."
        )

    # Store for restoring later
    original_forward = LongformerSelfAttention.forward

    LongformerSelfAttention.forward = args_to_func[key]

    example_inputs = (input_ids, attention_mask, global_attention_mask)

    Path(onnx_model_path).parent.mkdir(parents=True, exist_ok=True)

    torch_onnx_export(
        model,
        example_inputs,
        onnx_model_path,
        opset_version=12,
        input_names=["input_ids", "attention_mask", "global_attention_mask"],
        output_names=["last_state", "pooler"],
        dynamic_axes={
            "input_ids": {0: "batch_size", 1: "sequence_length"},
            "attention_mask": {0: "batch_size", 1: "sequence_length"},
            "global_attention_mask": {0: "batch_size", 1: "sequence_length"},
            "last_state": {0: "batch_size", 1: "sequence_length"},
            "pooler": {0: "batch_size", 1: "sequence_length"},
        },
        custom_opsets={"com.microsoft": 1},
    )
    print(f"ONNX model exported to {onnx_model_path}")

    # Restore original implementation:
    LongformerSelfAttention.forward = original_forward

