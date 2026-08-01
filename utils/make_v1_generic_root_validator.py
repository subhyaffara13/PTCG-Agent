
def make_v1_generic_root_validator(
    validator: V1RootValidatorFunction, pre: bool
) -> V2CoreBeforeRootValidator | V2CoreAfterRootValidator:
    """Wrap a V1 style root validator for V2 compatibility.

    Args:
        validator: The V1 style field validator.
        pre: Whether the validator is a pre validator.

    Returns:
        A wrapped V2 style validator.
    """
    if pre is True:
        # mode='before' for pydantic-core
        def _wrapper1(values: RootValidatorValues, _: core_schema.ValidationInfo) -> RootValidatorValues:
            return validator(values)

        return _wrapper1

    # mode='after' for pydantic-core
    def _wrapper2(fields_tuple: RootValidatorFieldsTuple, _: core_schema.ValidationInfo) -> RootValidatorFieldsTuple:
        if len(fields_tuple) == 2:
            # dataclass, this is easy
            values, init_vars = fields_tuple
            values = validator(values)
            return values, init_vars
        else:
            # ugly hack: to match v1 behaviour, we merge values and model_extra, then split them up based on fields
            # afterwards
            model_dict, model_extra, fields_set = fields_tuple
            if model_extra:
                fields = set(model_dict.keys())
                model_dict.update(model_extra)
                model_dict_new = validator(model_dict)
                for k in list(model_dict_new.keys()):
                    if k not in fields:
                        model_extra[k] = model_dict_new.pop(k)
            else:
                model_dict_new = validator(model_dict)
            return model_dict_new, model_extra, fields_set

    return _wrapper2

