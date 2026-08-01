
def _get_transform_spec(reason: Expression) -> DataclassTransformSpec:
    """Find the relevant transform parameters from the decorator/parent class/metaclass that
    triggered the dataclasses plugin.

    Although the resulting DataclassTransformSpec is based on the typing.dataclass_transform
    function, we also use it for traditional dataclasses.dataclass classes as well for simplicity.
    In those cases, we return a default spec rather than one based on a call to
    `typing.dataclass_transform`.
    """
    if _is_dataclasses_decorator(reason):
        return _TRANSFORM_SPEC_FOR_DATACLASSES

    spec = find_dataclass_transform_spec(reason)
    assert spec is not None, (
        "trying to find dataclass transform spec, but reason is neither dataclasses.dataclass nor "
        "decorated with typing.dataclass_transform"
    )
    return spec

