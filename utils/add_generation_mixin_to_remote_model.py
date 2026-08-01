
def add_generation_mixin_to_remote_model(model_class):
    """
    Adds `GenerationMixin` to the inheritance of `model_class`, if `model_class` is a PyTorch model.

    This function is used for backwards compatibility purposes: in v4.45, we've started a deprecation cycle to make
    `PreTrainedModel` stop inheriting from `GenerationMixin`. Without this function, older models dynamically loaded
    from the Hub may not have the `generate` method after we remove the inheritance.
    """
    # 1. If it is not a PT model (i.e. doesn't inherit Module), do nothing
    if "torch.nn.modules.module.Module" not in str(model_class.__mro__):
        return model_class

    # 2. If it already **directly** inherits from GenerationMixin, do nothing
    if "GenerationMixin" in str(model_class.__bases__):
        return model_class

    # 3. Prior to v4.45, we could detect whether a model was `generate`-compatible if it had its own `generate` and/or
    # `prepare_inputs_for_generation` method.
    has_custom_generate_in_class = hasattr(model_class, "generate") and "GenerationMixin" not in str(
        getattr(model_class, "generate")
    )
    has_custom_prepare_inputs = hasattr(model_class, "prepare_inputs_for_generation") and "GenerationMixin" not in str(
        getattr(model_class, "prepare_inputs_for_generation")
    )
    if has_custom_generate_in_class or has_custom_prepare_inputs:
        model_class_with_generation_mixin = type(
            model_class.__name__, (model_class, GenerationMixin), {**model_class.__dict__}
        )
        return model_class_with_generation_mixin
    return model_class

