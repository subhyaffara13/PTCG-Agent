
def register_agent(
    bus_name: str,
    *,
    perspective_flag: str = "player",
    needs_skills_dir: bool = True,
    needs_shared_context: bool = True,
):
    """
    Class decorator that registers a sub-agent for automatic discovery.

    Parameters
    ----------
    bus_name : str
        The name used when calling ``RouterBus.register_agent(bus_name, ...)``.
    perspective_flag : str
        The perspective flag passed to ``RouterBus.register_agent`` (default ``"player"``).
    needs_skills_dir : bool
        If True the orchestrator will pass ``skills_dir`` to the constructor.
    needs_shared_context : bool
        If True the orchestrator will pass ``shared_context`` to the constructor.
    """

    def decorator(cls: Type) -> Type:
        if bus_name in _AGENT_REGISTRY:
            registered_cls = _AGENT_REGISTRY[bus_name]['cls'].__name__
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


def register_agent(
    bus_name: str,
    *,
    perspective_flag: str = "player",
    needs_skills_dir: bool = True,
    needs_shared_context: bool = True,
):
    """
    Class decorator that registers a sub-agent for automatic discovery.

    Parameters
    ----------
    bus_name : str
        The name used when calling ``RouterBus.register_agent(bus_name, ...)``.
    perspective_flag : str
        The perspective flag passed to ``RouterBus.register_agent`` (default ``"player"``).
    needs_skills_dir : bool
        If True the orchestrator will pass ``skills_dir`` to the constructor.
    needs_shared_context : bool
        If True the orchestrator will pass ``shared_context`` to the constructor.
    """

    def decorator(cls: Type) -> Type:
        if bus_name in _AGENT_REGISTRY:
            registered_cls = _AGENT_REGISTRY[bus_name]['cls'].__name__
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


def register_agent(
    bus_name: str,
    *,
    perspective_flag: str = "player",
    needs_skills_dir: bool = True,
    needs_shared_context: bool = True,
):
    """
    Class decorator that registers a sub-agent for automatic discovery.

    Parameters
    ----------
    bus_name : str
        The name used when calling ``RouterBus.register_agent(bus_name, ...)``.
    perspective_flag : str
        The perspective flag passed to ``RouterBus.register_agent`` (default ``"player"``).
    needs_skills_dir : bool
        If True the orchestrator will pass ``skills_dir`` to the constructor.
    needs_shared_context : bool
        If True the orchestrator will pass ``shared_context`` to the constructor.
    """

    def decorator(cls: Type) -> Type:
        if bus_name in _AGENT_REGISTRY:
            registered_cls = _AGENT_REGISTRY[bus_name]['cls'].__name__
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

