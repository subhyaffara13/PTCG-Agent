import os

def envwrap(name, app="", types=None, is_method=False):
    """
    Basic (env-only) version of [envwrap](https://github.com/tqdm/envwrap).
    Install `envwrap` for config file support.
    """
    if types is None:
        types = {}
    if name[-1] == "_":
        name = name[:-1]
        warn("Trailing underscore in `name` is automatic", DeprecationWarning, stacklevel=2)
    prefixes = (name, f"{name}_{app}") if app else (name,)
    env_overrides = {}
    for prefix in prefixes:
        prefix = prefix.upper() + "_"
        i = len(prefix)
        env_overrides.update(
            (k[i:].lower(), v) for k, v in os.environ.items() if k.startswith(prefix))
    part = partialmethod if is_method else partial

    def wrap(func):
        params = signature(func).parameters
        # ignore unknown env vars
        overrides = {k: v for k, v in env_overrides.items() if k in params}
        # infer overrides' `type`s
        for k in overrides:
            param = params[k]
            if param.annotation is not param.empty:  # typehints
                for typ in getattr(param.annotation, '__args__', (param.annotation,)):
                    try:
                        overrides[k] = typ(overrides[k])
                    except Exception:  # nosec B110
                        pass
                    else:
                        break
            elif param.default is not None:  # type of default value
                overrides[k] = type(param.default)(overrides[k])
            else:
                try:  # `types` fallback
                    overrides[k] = types[k](overrides[k])
                except KeyError:  # keep unconverted (`str`)
                    pass
        return part(func, **overrides)
    return wrap

