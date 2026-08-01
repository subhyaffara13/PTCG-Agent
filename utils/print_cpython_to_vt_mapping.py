
def print_cpython_to_vt_mapping() -> None:
    """Print the mapping from CPython types to Dynamo VariableTracker classes.

    Reads _cpython_type from each VT subclass (own attribute only, not inherited).
    """
    # Ensure all VT modules are imported so all_subclasses is complete
    from . import (  # noqa: F401
        builtin,
        constant,
        ctx_manager,
        dicts,
        distributed,
        functions,
        higher_order_ops,
        iter,
        lazy,
        lists,
        misc,
        nn_module,
        streams,
        tensor,
        torch,
        torch_function,
        user_defined,
    )

    mapping: dict[type, list[type]] = {}
    for vt_cls in VariableTrackerMeta.all_subclasses:
        cpython_type = vt_cls.__dict__.get("_cpython_type")
        if cpython_type is None:
            continue
        types = cpython_type if isinstance(cpython_type, tuple) else (cpython_type,)
        for t in types:
            mapping.setdefault(t, []).append(vt_cls)

    for py_type, vt_classes in sorted(mapping.items(), key=lambda x: x[0].__qualname__):
        for vt_cls in vt_classes:
            print(
                f"{py_type.__module__}.{py_type.__qualname__:30s} -> {vt_cls.__name__}"
            )

