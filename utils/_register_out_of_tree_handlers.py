
def _register_out_of_tree_handlers() -> None:
    discovered_handler_generators = entry_points(group="torchrun.handlers")

    for handler_generator in discovered_handler_generators:
        try:
            # pyrefly: ignore [bad-index]
            get_handler = discovered_handler_generators[handler_generator.name].load()
            handler_registry.register(handler_generator.name, get_handler())
        except Exception:
            log.warning(
                "Exception while registering out of tree plugin %s: ",
                handler_generator.name,
                exc_info=True,
            )

