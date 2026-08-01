
def get_keys_to_not_convert(model) -> list:
    r"""
    Function to automatically detect keys to not convert for usage like quantization. For example for CausalLM modules
    we may want to keep the lm_head in full precision for numerical stability reasons.
    """
    # remove tied weights
    tied_keys = set()
    if len(model.all_tied_weights_keys) > 0:
        tied_keys = set(model.all_tied_weights_keys.values()) | set(model.all_tied_weights_keys.keys())

    # remove last module
    last_module_key = {list(model.named_parameters())[-1][0]}

    # remove output emb
    output_emb_module = model.get_output_embeddings()
    output_emb_keys = {
        name
        for name, module in model.named_modules()
        if output_emb_module is not None and id(module) == id(output_emb_module)
    }
    modules_to_not_convert = tied_keys | last_module_key | output_emb_keys

    modules_to_not_convert = list({k.removesuffix(".weight") for k in modules_to_not_convert})

    return list(modules_to_not_convert)

