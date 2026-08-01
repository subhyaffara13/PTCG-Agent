
def revert_weight_conversion(model: PreTrainedModel, state_dict: dict[str, torch.Tensor]):
    """
    Revert the conversion mapping that was used to load the model with `from_pretrained`, or the default one
    if the model was created in another way and is part of the default mappings.
    """
    weight_conversions = getattr(model, "_weight_conversions", None)
    # In this case, the model was not created with `from_pretrained` -> let's check if it's in the hardcoded
    # mappings, and recreate the mapping from there if it is
    if weight_conversions is None:
        from .conversion_mapping import get_model_conversion_mapping

        # Do not resave with the legacy renaming, if present
        weight_conversions = get_model_conversion_mapping(model, add_legacy=False)
        # If the model had no `_weight_conversions` attached, drop any PrefixChange transform - this is because the
        # model was almost surely instantiated from scratch (at least not from `from_pretrained`), and PrefixChange with
        # `prefix_to_remove` would otherwise add a unwanted prefix (as we dont have any information about whether the prefix
        # was there or not during load)
        weight_conversions = [x for x in weight_conversions if not isinstance(x, PrefixChange)]
        weight_conversions = weight_conversions if len(weight_conversions) > 0 else None

    # We did not find any operations to perform -> quick escape
    if weight_conversions is None:
        return state_dict

    # Important: we need to revert the order here, so that potential conversions from submodels are performed first
    weight_conversions = weight_conversions[::-1]

    # Two-phase save: first reverse converters, then reverse renamings. Relies on the rule that
    # WeightRenamings never operate on WeightConverter outputs (see WeightTransform docstring).
    inverted_transforms = [transform.reverse_transform() for transform in weight_conversions]
    inverted_converters = [transform for transform in inverted_transforms if isinstance(transform, WeightConverter)]
    inverted_renamings = [transform for transform in inverted_transforms if not isinstance(transform, WeightConverter)]
    pattern_to_converter = {
        pattern: converter for converter in inverted_converters for pattern in converter.source_patterns
    }

    conversion_mapping: dict[str, WeightTransform] = {}
    state_dict = sorted(state_dict.items(), key=lambda kv: dot_natural_key(kv[0]))
    for original_key, tensor in state_dict:
        # `converter_key`: key after phase-1 (converter namespace, used as layer_name by convert()).
        # `checkpoint_key`: key after phase-2 (final saved name, layer_name for plain renamings).
        converter_key, matched_pattern = rename_source_key(original_key, [], inverted_converters)
        checkpoint_key, _ = rename_source_key(converter_key, inverted_renamings, [])

        if matched_pattern is not None:
            # Bucket under converter_key so all sibling inputs land in the same converter instance.
            mapping = conversion_mapping.setdefault(converter_key, deepcopy(pattern_to_converter[matched_pattern]))
        else:
            mapping = conversion_mapping.setdefault(checkpoint_key, WeightRenaming(original_key, checkpoint_key))
            matched_pattern = original_key

        mapping.add_tensor(checkpoint_key, original_key, matched_pattern, tensor)

    new_state_dict = {}
    for layer_name, mapping in conversion_mapping.items():
        realized = mapping.convert(layer_name, model=model, config=model.config)
        for target_name, param in realized.items():
            param = param[0] if isinstance(param, list) else param
            if isinstance(mapping, WeightConverter):
                # Bring converter outputs from converter namespace into checkpoint namespace.
                target_name, _ = rename_source_key(target_name, inverted_renamings, [])
            new_state_dict[target_name] = param

    return new_state_dict

