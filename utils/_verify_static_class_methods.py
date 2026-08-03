from typing import Any

def _verify_static_class_methods(
    stub: nodes.FuncBase, runtime: Any, static_runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[str]:
    if stub.name in ("__new__", "__init_subclass__", "__class_getitem__"):
        # Special cased by Python, so don't bother checking
        return
    if inspect.isbuiltin(runtime):
        # The isinstance checks don't work reliably for builtins, e.g. datetime.datetime.now, so do
        # something a little hacky that seems to work well
        probably_class_method = isinstance(getattr(runtime, "__self__", None), type)
        if probably_class_method and not stub.is_class:
            yield "runtime is a classmethod but stub is not"
        if not probably_class_method and stub.is_class:
            yield "stub is a classmethod but runtime is not"
        return

    if static_runtime is MISSING:
        return

    if isinstance(static_runtime, classmethod) and not stub.is_class:
        yield "runtime is a classmethod but stub is not"
    if not isinstance(static_runtime, classmethod) and stub.is_class:
        yield "stub is a classmethod but runtime is not"
    if isinstance(static_runtime, staticmethod) and not stub.is_static:
        yield "runtime is a staticmethod but stub is not"
    if not isinstance(static_runtime, staticmethod) and stub.is_static:
        yield "stub is a staticmethod but runtime is not"

