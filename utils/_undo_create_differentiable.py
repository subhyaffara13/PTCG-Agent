
def _undo_create_differentiable(inps: _TensorsT, level: int | None = None) -> _TensorsT:
    def unwrap_tensors(x: _TensorsU) -> _TensorsU:
        if isinstance(x, torch.Tensor):
            if level is None:
                raise AssertionError("level must not be None when unwrapping tensors")
            # pyrefly: ignore[bad-return]
            return _unwrap_for_grad(x, level)
        # TODO: Remove the following hack for namedtuples
        if isinstance(x, tuple):
            return tree_map(unwrap_tensors, tuple(x))

        raise RuntimeError(f"Expected tensors, got unsupported type {type(x)}")

    return tree_map(unwrap_tensors, inps)

