
def check_no_bool_index_tensors(
    func: OpOverload, self: FakeTensor, indices: list[FakeTensor | None]
) -> None:
    for index in indices:
        if index is not None and index.dtype in (torch.bool, torch.uint8):
            raise DynamicOutputShapeException(func)

