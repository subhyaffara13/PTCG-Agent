import functools

def delegate_xp(delegator, module_name):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            xp = delegator(*args, **kwds)

            # try delegating to a cupyx/jax namesake
            if is_cupy(xp) and func.__name__ not in CUPY_BLOCKLIST:
                # https://github.com/cupy/cupy/issues/8336
                import importlib
                cupyx_module = importlib.import_module(f"cupyx.scipy.{module_name}")
                cupyx_func = getattr(cupyx_module, func.__name__)
                return cupyx_func(*args, **kwds)
            elif is_jax(xp) and func.__name__ == "map_coordinates":
                spx = scipy_namespace_for(xp)
                jax_module = getattr(spx, module_name)
                jax_func = getattr(jax_module, func.__name__)
                return jax_func(*args, **kwds)
            else:
                # the original function (does all np.asarray internally)
                # XXX: output arrays
                result = func(*args, **kwds)

                if isinstance(result, np.ndarray | np.generic):
                    # XXX: np.int32->np.array_0D
                    return xp.asarray(result)
                elif isinstance(result, int):
                    return result
                elif isinstance(result, dict):
                    # value_indices:
                    # result is {np.int64(1): (array(0), array(1))} etc
                    return {
                        k.item(): tuple(xp.asarray(vv) for vv in v)
                        for k,v in result.items()
                    }
                elif result is None:
                    # inplace operations
                    return result
                else:
                    # lists/tuples
                    return _maybe_convert_arg(result, xp)
        return wrapper
    return inner


def delegate_xp(delegator, module_name):
    def inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            try:
                xp = delegator(*args, **kwds)
            except TypeError:
                # object arrays
                if func.__name__ == "tf2ss":
                    import numpy as np
                    xp = np
                else:
                    raise

            # try delegating to a cupyx/jax namesake
            if is_cupy(xp) and func.__name__ not in CUPY_BLACKLIST:
                func_name = CUPY_RENAMES.get(func.__name__, func.__name__)

                # https://github.com/cupy/cupy/issues/8336
                import importlib
                cupyx_module = importlib.import_module(f"cupyx.scipy.{module_name}")
                cupyx_func = getattr(cupyx_module, func_name)
                kwds.pop('xp', None)
                return cupyx_func(*args, **kwds)
            elif is_jax(xp) and func.__name__ in JAX_SIGNAL_FUNCS:
                spx = scipy_namespace_for(xp)
                jax_module = getattr(spx, module_name)
                jax_func = getattr(jax_module, func.__name__)
                kwds.pop('xp', None)
                return jax_func(*args, **kwds)
            else:
                # the original function
                return func(*args, **kwds)
        return wrapper
    return inner

