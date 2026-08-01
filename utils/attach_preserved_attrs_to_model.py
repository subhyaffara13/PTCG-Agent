
def attach_preserved_attrs_to_model(
    model: GraphModule | torch.nn.Module,
    preserved_attrs: dict[str, Any],
) -> None:
    """Store preserved attributes to the model.meta so that it can be preserved during deepcopy"""
    model.meta[_USER_PRESERVED_ATTRIBUTES_KEY] = copy.copy(preserved_attrs)  # type: ignore[operator, index, assignment]
    # set the preserved attributes in the model so that user can call
    # model.attr as they do before calling fx graph mode quantization
    for attr_name, attr in model.meta[_USER_PRESERVED_ATTRIBUTES_KEY].items():  # type: ignore[index, union-attr]
        setattr(model, attr_name, attr)

