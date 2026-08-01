
def _defaultdict_deserialize(dumpable_context: DumpableContext) -> Context:
    if not isinstance(dumpable_context, dict):
        raise AssertionError("dumpable_context must be a dict")

    expected_keys = {
        "default_factory_module",
        "default_factory_name",
        "dict_context",
    }
    if set(dumpable_context) != expected_keys:
        raise AssertionError(
            f"dumpable_context keys must be {expected_keys}, got {set(dumpable_context)}"
        )

    default_factory_module = dumpable_context["default_factory_module"]
    default_factory_name = dumpable_context["default_factory_name"]
    if not isinstance(default_factory_module, str):
        raise AssertionError("default_factory_module must be a string")
    if not isinstance(default_factory_name, str):
        raise AssertionError("default_factory_name must be a string")
    module = importlib.import_module(default_factory_module)
    default_factory = getattr(module, default_factory_name)

    dict_context = dumpable_context["dict_context"]
    return [default_factory, dict_context]

