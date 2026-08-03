from typing import Dict

def gather_all_validators(type_: 'ModelOrDc') -> Dict[str, 'AnyClassMethod']:
    all_attributes = ChainMap(*[cls.__dict__ for cls in type_.__mro__])  # type: ignore[arg-type,var-annotated]
    return {
        k: v
        for k, v in all_attributes.items()
        if hasattr(v, VALIDATOR_CONFIG_KEY) or hasattr(v, ROOT_VALIDATOR_CONFIG_KEY)
    }

