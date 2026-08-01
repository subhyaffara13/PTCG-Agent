
def _get_arg_dtype(arg: torch.fx.Node) -> t.Any:
    if not isinstance(arg, torch.fx.Node):
        raise AssertionError(f"Expected torch.fx.Node, got {type(arg)}")
    tensor_meta = arg.meta.get("tensor_meta")  # type: ignore[union-attr]
    dtype = (
        tensor_meta.dtype
        if isinstance(tensor_meta, TensorMetadata)
        else arg.meta["type"]
    )
    return dtype

