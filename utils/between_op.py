
def between_op(data: Any, dim: str, lower: int, upper: int) -> bool:
    return data[dim] >= lower and data[dim] <= upper

