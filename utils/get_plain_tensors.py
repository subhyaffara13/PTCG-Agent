
def get_plain_tensors(
    subclass: Tensor, *, out: list[Tensor | int | SymInt | OpaqueBase]
) -> list[Tensor | int | SymInt | OpaqueBase]:
    # This function is used in Runtime, do not add redundant asserts
    todo = [subclass]
    while todo:
        curr = todo.pop()
        if not is_traceable_wrapper_subclass(curr):
            out.append(curr)
            continue

        inner_keys, _ = curr.__tensor_flatten__()
        todo.extend(getattr(curr, key) for key in reversed(inner_keys))

    return out

