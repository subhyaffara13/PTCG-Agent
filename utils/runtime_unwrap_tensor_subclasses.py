
def runtime_unwrap_tensor_subclasses(
    wrapped_args: list[Tensor | int],
    *,
    append_symints: bool,
    subclass_metas: list[PlainTensorMeta | SubclassCreationMeta] | None = None,
) -> list[int | Tensor | SymInt | OpaqueBase]:
    def flatten_subclass(
        x: Tensor,
        subclass_meta: PlainTensorMeta | SubclassCreationMeta | OpaqueMeta | None,
        *,
        out: list[OpaqueBase | SymInt | Tensor | int],
    ) -> list[OpaqueBase | SymInt | Tensor | int]:
        if not is_traceable_wrapper_subclass(x):
            out.append(x)
            return out

        if not isinstance(x, Tensor):
            raise AssertionError(f"expected Tensor, got {type(x)}")
        if not isinstance(subclass_meta, SubclassCreationMeta):
            raise AssertionError("subclass_meta should be a SubclassCreationMeta")

        attrs, _ = x.__tensor_flatten__()

        for attr in attrs:
            inner_value = getattr(x, attr)
            match inner_value:
                case OpaqueBase():
                    out.append(inner_value)
                case Tensor():
                    inner_meta = subclass_meta.attrs.get(attr)
                    flatten_subclass(inner_value, inner_meta, out=out)
                case _:
                    raise AssertionError(
                        f"expected Tensor or OpaqueBase, got {type(inner_value)}"
                    )

        if append_symints:
            # outer_size
            size = x.size()
            symint_placeholders = compute_symint_placeholders(subclass_meta.outer_size)
            if len(size) != len(symint_placeholders):
                raise AssertionError(
                    f"size length mismatch: {len(size)} != {len(symint_placeholders)}"
                )
            out.extend(
                [r for (r, is_symint) in zip(size, symint_placeholders) if is_symint]
            )

            # outer_stride
            stride = x.stride()
            symint_placeholders = compute_symint_placeholders(
                subclass_meta.outer_stride
            )
            if len(stride) != len(symint_placeholders):
                raise AssertionError(
                    f"stride length mismatch: {len(stride)} != {len(symint_placeholders)}"
                )
            out.extend(
                [r for (r, is_symint) in zip(stride, symint_placeholders) if is_symint]
            )
        return out

    xs_inner: list[int | Tensor | SymInt | OpaqueBase] = []

    if append_symints:
        if subclass_metas is None:
            raise AssertionError(
                "subclass_metas must not be None when append_symints is True"
            )

    for idx, x in enumerate(wrapped_args):
        if not is_traceable_wrapper_subclass(x):
            xs_inner.append(x)
            continue

        if subclass_metas is None:
            get_plain_tensors(typing.cast(Tensor, x), out=xs_inner)
        else:
            subclass_meta = subclass_metas[idx]
            if not isinstance(subclass_meta, SubclassCreationMeta):
                raise AssertionError(
                    f"expected SubclassCreationMeta, got {type(subclass_meta)}"
                )
            flatten_subclass(typing.cast(Tensor, x), subclass_meta, out=xs_inner)

    return xs_inner

