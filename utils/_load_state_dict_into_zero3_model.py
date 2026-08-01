
def _load_state_dict_into_zero3_model(model_to_load, state_dict, load_config=None):
    """
    Loads state dict into a model specifically for Zero3, since DeepSpeed does not support the `transformers`
    tensor parallelism API.

    Nearly identical code to PyTorch's `_load_from_state_dict`

    Args:
        model_to_load: The model to load weights into
        state_dict: The state dict containing the weights
        load_config: Optional LoadStateDictConfig containing weight_mapping and other loading options
    """
    # copy state_dict so `_load_state_dict_into_zero3_model` can modify it
    metadata = getattr(state_dict, "_metadata", None)
    state_dict = state_dict.copy()
    if metadata is not None:
        state_dict._metadata = metadata

    # Extract weight_mapping from load_config if provided
    weight_mapping = None
    if load_config is not None:
        weight_mapping = getattr(load_config, "weight_mapping", None)

    # Apply weight conversions if provided
    if weight_mapping is not None and len(weight_mapping) > 0:
        state_dict = _apply_weight_conversions_to_state_dict(model_to_load, state_dict, weight_mapping)
        # Keep the current weight conversion mapping for later saving (in case it was coming directly from the user)
        model_to_load._weight_conversions = weight_mapping

    error_msgs = []
    meta_model_state_dict = model_to_load.state_dict()
    missing_keys = set(meta_model_state_dict.keys())

    prefix_model = getattr(model_to_load, "base_model_prefix", None)
    # take care of the case where in the checkpoint we don't have the prefix
    state_dict = {
        (f"{prefix_model}.{k}" if meta_model_state_dict.get(f"{prefix_model}.{k}") is not None else k): v
        for k, v in state_dict.items()
    }

    # PyTorch's `_load_from_state_dict` does not copy parameters in a module's descendants
    # so we need to apply the function recursively.
    def load(module: nn.Module, state_dict, prefix="", assign_to_params_buffers=False):
        local_metadata = {} if metadata is None else metadata.get(prefix[:-1], {})
        local_metadata["assign_to_params_buffers"] = assign_to_params_buffers

        args = (state_dict, prefix, local_metadata, True, [], [], error_msgs)
        # Parameters of module and children will start with prefix. We can exit early if there are none in this
        # state_dict
        if is_deepspeed_zero3_enabled():
            import deepspeed

            # In sharded models, each shard has only part of the full state_dict, so only gather
            # parameters that are in the current state_dict.
            named_parameters = dict(module.named_parameters(prefix=prefix[:-1], recurse=False))
            params_to_gather = []
            for k in named_parameters:
                if k in state_dict:
                    param = named_parameters[k]
                    # crucial to not init the weight again
                    param._is_hf_initialized = True
                    params_to_gather.append(param)
                    missing_keys.discard(k)

            if len(params_to_gather) > 0:
                # because zero3 puts placeholders in model params, this context
                # manager gathers (unpartitions) the params of the current layer, then loads from
                # the state dict and then re-partitions them again
                with deepspeed.zero.GatheredParameters(params_to_gather, modifier_rank=0):
                    if torch.distributed.get_rank() == 0:
                        module._load_from_state_dict(*args)

            # Buffers are not partitioned by ZeRO-3, load them directly
            named_buffers = dict(module.named_buffers(prefix=prefix[:-1], recurse=False))
            for k, buf in named_buffers.items():
                if k in state_dict and buf is not None:
                    missing_keys.discard(k)
                    with torch.no_grad():
                        buf.copy_(state_dict[k])
                    buf._is_hf_initialized = True

        for name, child in module._modules.items():
            if child is not None:
                load(child, state_dict, prefix + name + ".", assign_to_params_buffers)

    load(model_to_load, state_dict, assign_to_params_buffers=False)

    return error_msgs, missing_keys

