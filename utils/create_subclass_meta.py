from typing import Any

def create_subclass_meta(
    curr_args: list[Any] | tuple[Any, ...],
    *,
    count_symints: bool = True,
    with_memory_format: bool = False,
) -> list[PlainTensorMeta | SubclassCreationMeta]:
    idx = 0
    infos: list[PlainTensorMeta | SubclassCreationMeta] = []
    for a in curr_args:
        if is_traceable_wrapper_subclass(a):
            if not isinstance(a, Tensor):
                raise AssertionError(
                    f"expected Tensor for traceable wrapper subclass, got {type(a)}"
                )
            start_idx = idx
            subclass_meta, _ = create_subclass_metadata(
                a,
                start_idx,
                count_symints=count_symints,
                with_memory_format=with_memory_format,
            )
            infos.append(subclass_meta)
            cnt = subclass_meta.arg_count
        else:
            infos.append(
                PlainTensorMeta(
                    idx,
                    memory_format=maybe_suggest_memory_format(a, with_memory_format),
                )
            )
            cnt = 1
        idx += cnt
    return infos

