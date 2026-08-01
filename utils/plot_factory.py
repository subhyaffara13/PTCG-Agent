
def plot_factory(*args, **kwargs):
    backend = kwargs.pop("backend", "default")
    if isinstance(backend, str):
        if backend == "default":
            matplotlib = import_module('matplotlib',
                min_module_version='1.1.0', catch=(RuntimeError,))
            if matplotlib:
                return MatplotlibBackend(*args, **kwargs)
            return TextBackend(*args, **kwargs)
        return plot_backends[backend](*args, **kwargs)
    elif (type(backend) == type) and issubclass(backend, Plot):
        return backend(*args, **kwargs)
    else:
        raise TypeError("backend must be either a string or a subclass of ``Plot``.")

