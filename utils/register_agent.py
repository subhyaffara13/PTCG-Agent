from typing import Type

def register_agent(
    bus_name: str,
    *,
    perspective_flag: str = "player",
    needs_skills_dir: bool = True,
    needs_shared_context: bool = True,
):
    """
    Class decorator that registers a sub-agent for automatic discovery.
    """
    from cb_agents.registry import _AGENT_REGISTRY

    def decorator(cls: Type) -> Type:
        if bus_name in _AGENT_REGISTRY:
            registered_cls = _AGENT_REGISTRY[bus_name]['cls'].__name__
            if registered_cls != cls.__name__:
                raise ValueError(
                    f"Duplicate agent registration: bus_name '{bus_name}' "
                    f"is already registered to {registered_cls}"
                )
        _AGENT_REGISTRY[bus_name] = {
            "cls": cls,
            "perspective_flag": perspective_flag,
            "needs_skills_dir": needs_skills_dir,
            "needs_shared_context": needs_shared_context,
        }
        return cls

    return decorator
