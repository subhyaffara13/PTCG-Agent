
def convert_to_concrete_values(size_or_stride: list[Any]) -> list[int | None]:
    return [convert_int_to_concrete_values(dim) for dim in size_or_stride]

