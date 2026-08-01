
def get_model_conversion_mapping(
    model: PreTrainedModel,
    key_mapping: dict[str, str] | None = None,
    hf_quantizer: HfQuantizer | None = None,
    add_legacy: bool = True,
) -> list[WeightTransform]:
    """
    Collect the ordered list of weight transforms for `model` (used during
    loading and, when reversed, during saving).

    Each `PreTrainedModel` sub-module is looked up by class name then
    `model_type`.  Root transforms are applied globally; sub-module transforms
    have their `scope_prefix` set so they only match keys under that prefix.  After any
    sub-module is processed, both its class name and `model_type` are marked
    seen to prevent `XForY` / `XModel` pairs from applying the same mapping
    twice via different lookup paths.
    """
    from .modeling_utils import PreTrainedModel

    # note: this function is used in PEFT, so changing the API requires coordination
    weight_conversions = []

    # Load models with explicit, user-provided key mapping
    if key_mapping is not None:
        weight_conversions = [WeightRenaming(source_patterns=k, target_patterns=v) for k, v in key_mapping.items()]

    # Maps each identifier (class name or model_type) to the module paths that have
    # already claimed it.  A later module is skipped only when one of those paths is
    # an ancestor of the current module path — siblings are never ancestors of each
    # other, so two sibling sub-models with the same model_type both get their own
    # scoped transforms.  A child is an ancestor of everything nested under it, which
    # prevents a parent's transforms from being duplicated with a scoped copy for the child.
    seen_identifiers: defaultdict[str, list[str]] = defaultdict(list)

    for module_name, submodule in model.named_modules():
        # Skip if it's not a submodel
        if not isinstance(submodule, PreTrainedModel):
            continue

        class_name = type(submodule).__name__
        model_type = submodule.config.model_type

        # Skip if an ancestor already claimed this class (its unscoped transforms already cover this subtree).
        if any(seen == "" or module_name.startswith(seen + ".") for seen in seen_identifiers[class_name]):
            continue

        # Class name takes priority — a class-specific mapping bypasses the model_type
        # deduplication check (e.g. LlavaModel nested inside LlavaForConditionalGeneration
        # must still get its own scoped mapping even after "llava" is marked seen).
        conversions = get_checkpoint_conversion_mapping(class_name)
        found_via_class = conversions is not None

        if not found_via_class:
            # Same ancestor check as above, but via model_type for modules without a class-specific mapping.
            if model_type and any(
                seen == "" or module_name.startswith(seen + ".") for seen in seen_identifiers[model_type]
            ):
                continue
            if model_type is not None:
                conversions = get_checkpoint_conversion_mapping(model_type)

        if conversions is None:
            continue

        is_root_model = module_name == ""
        if not is_root_model:
            # Scope each transform so it only matches keys under this sub-module's prefix - but we still allow to
            # arbitrary add/remove base_model_prefix to load ForXXX model from BaseModel and the opposite
            # Note that we need 2 removeprefix calls here, as only one level of nesting would not have the ending dot to module_name
            scope_prefix = module_name.removeprefix(model.base_model_prefix)
            scope_prefix = module_name.removeprefix(".")
            for transform in conversions:
                transform.scope_prefix = scope_prefix
                transform.base_model_prefix = model.base_model_prefix
        weight_conversions.extend(conversions)

        seen_identifiers[class_name].append(module_name)
        # Only record model_type when the hit was via model_type. When the hit was via
        # class name, other sub-modules sharing the same model_type but without a
        # class-specific mapping (e.g. DetrModel under DetrForSegmentation) must still
        # be reachable so their base transforms are picked up and scoped.
        if not found_via_class and model_type:
            seen_identifiers[model_type].append(module_name)

    if add_legacy:
        weight_conversions.extend(get_checkpoint_conversion_mapping("legacy"))

    # Let the quantizer rewrite / augment the conversion pipeline. This is where the
    # FP8 dequantizer (when `dequantize=True`) prepends a `Fp8Dequantize` op to
    # every existing converter so that per-block scales are applied *before* any
    # expert-merge / concat ops flatten the per-expert structure away.
    if hf_quantizer is not None:
        weight_conversions = hf_quantizer.update_weight_conversions(weight_conversions)

    return weight_conversions

