
def patch_moe_parameter_targeting(model, peft_config):
    """PEFT currently assumes that expert layers are of shape
        (expert, in, out)
    but with Mixtral in transformers v5 this is not true anymore.
    This will be addressed in PEFT >0.19 until then we need to handle
    it here for now.
    """
    from functools import wraps

    import peft

    model_type = getattr(model.config, "model_type", None)
    if get_checkpoint_conversion_mapping(model_type) is not None:
        update_layer = peft.tuners.lora.layer.ParamWrapper.update_layer

        @wraps(update_layer)
        def new_update_layer(layer, *args, **kwargs):
            did_swap = getattr(layer, "_did_swap_in_out_features", False)
            if not did_swap and layer.parameter_name in ("down_proj", "gate_up_proj"):
                tmp_in_features = layer.in_features
                layer.in_features = layer.out_features
                layer.out_features = tmp_in_features
                layer._did_swap_in_out_features = True
            return update_layer(layer, *args, **kwargs)

        peft.tuners.lora.layer.ParamWrapper.update_layer = new_update_layer

