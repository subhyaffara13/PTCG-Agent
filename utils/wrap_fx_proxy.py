from typing import Any

def wrap_fx_proxy(
    tx: "InstructionTranslatorBase",
    proxy: Any,
    example_value: Any | None = None,
    subclass_type: type | None = None,
    **options: Any,
) -> VariableTracker:
    kwargs = {
        "tx": tx,
        "proxy": proxy,
        "example_value": example_value,
        "subclass_type": subclass_type,
        **options,
    }
    if subclass_type is None:
        # pyrefly: ignore[bad-argument-type]
        return wrap_fx_proxy_cls(target_cls=TensorVariable, **kwargs)
    else:
        # pyrefly: ignore[bad-argument-type]
        result = wrap_fx_proxy_cls(target_cls=TensorWithTFOverrideVariable, **kwargs)
        # type: ignore[attr-defined]
        result.install_global(tx)
        return result

