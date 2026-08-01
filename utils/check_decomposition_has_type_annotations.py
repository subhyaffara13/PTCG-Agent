
def check_decomposition_has_type_annotations(f) -> None:
    inspect_empty = inspect._empty  # type: ignore[attr-defined]
    sig = inspect.signature(f)
    for param in sig.parameters.values():
        if param.annotation == inspect_empty:
            raise AssertionError(
                f"No signature on param {param.name} for function {f.name}"
            )

    if sig.return_annotation == inspect_empty:
        raise AssertionError(f"No return annotation for function {f.name}")

