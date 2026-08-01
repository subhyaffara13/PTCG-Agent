
def input_dtypes(event: _ProfilerEvent):
    if not isinstance(event.extra_fields, _ExtraFields_TorchOp):
        raise AssertionError(
            f"expected _ExtraFields_TorchOp, got {type(event.extra_fields).__name__}"
        )
    return tuple(getattr(i, "dtype", None) for i in event.extra_fields.inputs)

