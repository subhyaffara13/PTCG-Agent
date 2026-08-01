
def format_inputs_log(inputs: list[Any]) -> str:
    def format_item(i: int, inp: Any) -> str:
        if isinstance(inp, torch.Tensor):
            return (
                f"[{i}]: Tensor(size={list(inp.size())}, stride={inp.stride()}, "
                f"dtype={inp.dtype}, data_ptr=0x{inp.data_ptr():X})"
            )
        elif inp is None:
            return f"[{i}]: None"
        else:
            return f"[{i}]: {type(inp).__name__}({inp})"

    n = len(inputs)
    if n == 0:
        return "[]"

    # Only display the first 10 inputs if the input list is too long
    max_items = 10
    parts = [format_item(i, inp) for i, inp in enumerate(inputs[:max_items])]
    if n > max_items:
        parts.append(f"... ({n - max_items} more items)")

    return ", ".join(parts)

