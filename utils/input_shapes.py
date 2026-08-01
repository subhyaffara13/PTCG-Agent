
def input_shapes(event: _ProfilerEvent):
    if not isinstance(event.extra_fields, _ExtraFields_TorchOp):
        raise AssertionError(
            f"expected _ExtraFields_TorchOp, got {type(event.extra_fields).__name__}"
        )
    return tuple(tuple(getattr(i, "sizes", ())) for i in event.extra_fields.inputs)

