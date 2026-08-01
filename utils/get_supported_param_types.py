
def get_supported_param_types():
    data: list[tuple[type | typing._SpecialForm, str, bool, bool, bool]] = [
        # (python type, schema type, type[] variant, type?[] variant, type[]? variant
        (Tensor, "Tensor", True, True, False),
        (int, "SymInt", True, False, True),
        (float, "float", True, False, True),
        (bool, "bool", True, False, True),
        (str, "str", False, False, False),
        (types.Number, "Scalar", True, False, False),
        (dtype, "ScalarType", False, False, False),
        (device, "Device", False, False, False),
    ]

    if torch.distributed.is_available():
        from torch.distributed.distributed_c10d import GroupName

        data.append((typing.cast(type, GroupName), "str", False, False, False))

    result = []
    for line in data:
        result.extend(derived_types(*line))
    return dict(result)

