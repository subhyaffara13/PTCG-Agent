import os

def _set_configs_from_environment():
    """Initialize ``config.backend_priority``, load backend_info and config.

    This gets default values from environment variables (see ``nx.config`` for details).
    This function is run at the very end of importing networkx. It is run at this time
    to avoid loading backend_info before the rest of networkx is imported in case a
    backend uses networkx for its backend_info (e.g. subclassing the Config class.)
    """
    # backend_info is defined above as empty dict. Fill it after import finishes.
    backend_info.update(_get_backends("networkx.backend_info", load_and_call=True))
    backend_info.update(
        (backend, {}) for backend in backends.keys() - backend_info.keys()
    )

    # set up config based on backend_info and environment
    backend_config = {}
    for backend, info in backend_info.items():
        if "default_config" not in info:
            cfg = Config()
        else:
            cfg = info["default_config"]
            if not isinstance(cfg, Config):
                cfg = Config(**cfg)
        backend_config[backend] = cfg
    backend_config = Config(**backend_config)
    # Setting doc of backends_config type is not setting doc of Config
    # Config has __new__ method that returns instance with a unique type!
    type(backend_config).__doc__ = "All installed NetworkX backends and their configs."

    backend_priority = BackendPriorities(algos=[], generators=[], classes=[])

    config = NetworkXConfig(
        backend_priority=backend_priority,
        backends=backend_config,
        cache_converted_graphs=bool(
            os.environ.get("NETWORKX_CACHE_CONVERTED_GRAPHS", True)
        ),
        fallback_to_nx=bool(os.environ.get("NETWORKX_FALLBACK_TO_NX", False)),
        warnings_to_ignore=set(
            _comma_sep_to_list(os.environ.get("NETWORKX_WARNINGS_TO_IGNORE", ""))
        ),
    )

    # Add "networkx" item to backend_info now b/c backend_config is set up
    backend_info["networkx"] = {}

    # NETWORKX_BACKEND_PRIORITY is the same as NETWORKX_BACKEND_PRIORITY_ALGOS
    priorities = {
        key[26:].lower(): val
        for key, val in os.environ.items()
        if key.startswith("NETWORKX_BACKEND_PRIORITY_")
    }
    backend_priority = config.backend_priority
    backend_priority.algos = (
        _comma_sep_to_list(priorities.pop("algos"))
        if "algos" in priorities
        else _comma_sep_to_list(
            os.environ.get(
                "NETWORKX_BACKEND_PRIORITY",
                os.environ.get("NETWORKX_AUTOMATIC_BACKENDS", ""),
            )
        )
    )
    backend_priority.generators = _comma_sep_to_list(priorities.pop("generators", ""))
    for key in sorted(priorities):
        backend_priority[key] = _comma_sep_to_list(priorities[key])

    return config

