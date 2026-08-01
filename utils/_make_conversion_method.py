
def _make_conversion_method(name: str, dtype: torch.dtype):
    def fn(
        self: TensorLikeType, memory_format: torch.memory_format = torch.preserve_format
    ) -> TensorLikeType:
        return self.to(dtype, memory_format=memory_format)  # type: ignore[call-overload]

    fn.__name__ = name
    return fn

