
def register_adapter(
    aten: str | list[str],
) -> Callable[
    [AdapterType],
    AdapterType,
]:
    def decorator(func: AdapterType) -> AdapterType:
        # pyrefly: ignore [unknown-name]
        global _adapters_map

        if isinstance(aten, str):
            adapters_map[aten] = func
        else:
            for at in aten:
                adapters_map[at] = func
        return func

    return decorator

