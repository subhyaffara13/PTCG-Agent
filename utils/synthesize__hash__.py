
def synthesize__hash__(cls) -> ParsedDef:
    return compose_fn(
        cls,
        "__hash__",
        [
            # This is just a placeholder to prevent compilation from failing; this won't even get called at
            # all right now because the TorchScript interpreter doesn't call custom __hash__ implementations
            "raise NotImplementedError('__hash__ is not supported for dataclasses in TorchScript')"
        ],
        signature="(self) -> int",
    )

