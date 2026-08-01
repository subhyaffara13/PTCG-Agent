
def create_subclass_metadata(
    a: Any,
    start_idx: int,
    count_symints: bool,
    with_memory_format: bool = False,
) -> tuple[Any, int]:
    if not is_traceable_wrapper_subclass(a):
        idx = start_idx + 1
        return (
            PlainTensorMeta(
                idx,
                memory_format=maybe_suggest_memory_format(a, with_memory_format),
            ),
            idx,
        )

    inner_keys, metadata = a.__tensor_flatten__()
    new_start_idx = start_idx
    attrs: dict[str, SubclassCreationMeta | PlainTensorMeta | OpaqueMeta] = {}

    for key in inner_keys:
        inner_value = getattr(a, key)
        match inner_value:
            case OpaqueBase():
                # During tracing, opaques are wrapped in FakeScriptObject;
                # unwrap to check the real type.
                real_type = type(maybe_unwrap_fake_script_object(inner_value))
                if not is_opaque_reference_type(real_type):
                    raise RuntimeError(
                        f"{real_type.__name__!r} found in tensor attrs of "
                        f"{type(a).__name__}.__tensor_flatten__(). "
                        "Only tensors and reference-type opaques are allowed "
                        "in tensor attrs."
                    )
                attrs[key] = OpaqueMeta()
                new_start_idx += 1
            case Tensor():
                new_subclass_meta, new_start_idx = create_subclass_metadata(
                    inner_value,
                    new_start_idx,
                    count_symints=count_symints,
                    with_memory_format=with_memory_format,
                )
                attrs[key] = new_subclass_meta
            case _:
                raise AssertionError(
                    f"expected Tensor or OpaqueBase, got {type(inner_value)}"
                )

    # It *must* be because is_traceable_wrapper_subclass() - but mypy is not smart.
    if not isinstance(a, Tensor):
        raise AssertionError(f"expected Tensor, got {type(a)}")

    new_start_idx = (
        new_start_idx
        + count_symints * len(enumerate_filter_symints(a.size()))
        + count_symints * len(enumerate_filter_symints(a.stride()))
    )

    return (
        SubclassCreationMeta(
            flat_tensor_start_idx=start_idx,
            arg_count=new_start_idx - start_idx,
            included_subclass_symints=count_symints,
            attrs=attrs,
            meta=metadata,
            outer_size=a.size(),  # type: ignore[attr-defined, arg-type]
            outer_stride=a.stride(),  # type: ignore[arg-type]
            original_subclass=a,
            memory_format=maybe_suggest_memory_format(a, with_memory_format),
        ),
        new_start_idx,
    )

