from typing import Any

def _decorator_infos_for_class(
    typ: type[Any],
    *,
    collect_to_replace: bool,
) -> tuple[DecoratorInfos, list[tuple[str, Any]]]:
    """Collect a `DecoratorInfos` for class, without looking into bases."""
    res = DecoratorInfos()
    to_replace: list[tuple[str, Any]] = []

    for var_name, var_value in vars(typ).items():
        if isinstance(var_value, PydanticDescriptorProxy):
            info = var_value.decorator_info
            if isinstance(info, ValidatorDecoratorInfo):
                res.validators[var_name] = Decorator.build(typ, cls_var_name=var_name, shim=var_value.shim, info=info)
            elif isinstance(info, FieldValidatorDecoratorInfo):
                res.field_validators[var_name] = Decorator.build(
                    typ, cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, RootValidatorDecoratorInfo):
                res.root_validators[var_name] = Decorator.build(
                    typ, cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, FieldSerializerDecoratorInfo):
                res.field_serializers[var_name] = Decorator.build(
                    typ, cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelValidatorDecoratorInfo):
                res.model_validators[var_name] = Decorator.build(
                    typ, cls_var_name=var_name, shim=var_value.shim, info=info
                )
            elif isinstance(info, ModelSerializerDecoratorInfo):
                res.model_serializers[var_name] = Decorator.build(
                    typ, cls_var_name=var_name, shim=var_value.shim, info=info
                )
            else:
                from ..fields import ComputedFieldInfo

                isinstance(var_value, ComputedFieldInfo)
                res.computed_fields[var_name] = Decorator.build(typ, cls_var_name=var_name, shim=None, info=info)
            if collect_to_replace:
                to_replace.append((var_name, var_value.wrapped))

    return res, to_replace

