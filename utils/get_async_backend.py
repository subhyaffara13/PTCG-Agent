
def get_async_backend(asynclib_name: str | None = None) -> type[AsyncBackend]:
    if asynclib_name is None:
        asynclib_name = current_async_library()
        if not asynclib_name:
            raise NoEventLoopError(
                f"Not currently running on any asynchronous event loop. "
                f"Available async backends: {', '.join(get_all_backends())}"
            )

    # We use our own dict instead of sys.modules to get the already imported back-end
    # class because the appropriate modules in sys.modules could potentially be only
    # partially initialized
    try:
        return loaded_backends[asynclib_name]
    except KeyError:
        module = import_module(f"anyio._backends._{asynclib_name}")
        loaded_backends[asynclib_name] = module.backend_class
        return module.backend_class

