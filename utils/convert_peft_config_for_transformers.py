
def convert_peft_config_for_transformers(peft_config, model: torch.nn.Module, conversions: list[Any] | None):
    """
    Convert the PEFT config of models whose architecture changed from transformers v4 to v5.

    For most models, this requires no changes, this mostly affects some MoE models like Mixtral.
    """
    # If, for any reason, we cannot apply conversion, we just return the PEFT config as is.
    from peft import PeftType  # avoid circular import

    if peft_config.peft_type != PeftType.LORA:
        # weight conversion is currently only supported for LoRA
        return peft_config
    if not hasattr(model, "config"):
        # not a transformer model
        return peft_config
    if not hasattr(model.config, "model_type"):
        # not a transformer model
        return peft_config

    peft_config = copy.deepcopy(peft_config)  # don't mutate the original config
    model_type = getattr(model.config, "model_type", None)
    if get_checkpoint_conversion_mapping(model_type) is not None:
        peft_config = _convert_peft_config_moe(peft_config, model_type)

    return peft_config

