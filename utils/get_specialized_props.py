
def get_specialized_props(
    target_cls: Any,
    tx: "InstructionTranslatorBase",
    example_value: Any,
    subclass_type: type | None,
) -> dict[str, Any]:
    specialized_props = target_cls.specialize(example_value)
    # TODO: not sure about this fake mode test
    if (
        isinstance(example_value, torch._subclasses.fake_tensor.FakeTensor)
        and example_value.fake_mode is tx.fake_mode
    ):
        if subclass_type:
            tensor_type = subclass_type
        elif isinstance(example_value, torch.nn.Parameter):
            tensor_type = torch.nn.Parameter
        elif isinstance(example_value, torch.nn.Buffer):
            tensor_type = torch.nn.Buffer
        else:
            tensor_type = torch.Tensor
        specialized_props["class_type"] = tensor_type

    return specialized_props

