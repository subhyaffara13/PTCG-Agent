from typing import Callable, Dict

def register_protocol(default_params: Dict = None) -> Callable:
    """
    A decorator to register a protocol class in the central unified registry.
    The protocol is registered using its class name.
    """
    if default_params is None:
        default_params = {}

    def decorator(cls: Type) -> Type:
        name = cls.__name__
        if name in PROTOCOL_REGISTRY:
            raise TypeError(f"Protocol '{name}' is already registered.")

        PROTOCOL_REGISTRY[name] = {"class": cls, "default_params": default_params}
        return cls

    return decorator

