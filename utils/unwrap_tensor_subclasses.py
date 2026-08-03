from typing import Any, Callable

def unwrap_tensor_subclasses(
    wrapped_args: list[FxValue],
    wrapped_args_descs: Sequence[AOTDescriptor],
    *,
    append_symints: bool,
) -> tuple[list[FxValue], list[AOTDescriptor]]:
    def _maybe_fakeify_opaque(v: Any) -> Any:
        # Registered opaque types need to be wrapped as FakeScriptObject for
        # compile-time FX tracing (proxy slot tracking, hashability, etc.).
        if isinstance(v, OpaqueBase):
            from torch._guards import detect_fake_mode
            from torch._library.fake_class_registry import maybe_to_fake_obj
            from torch._library.opaque_object import is_opaque_type

            fake_mode = detect_fake_mode()
            if fake_mode is not None and is_opaque_type(type(v)):
                return maybe_to_fake_obj(fake_mode, v)
        return v

    def flatten_subclass(
        t: FxValue,
        desc: AOTDescriptor,
        *,
        out: tuple[list[FxValue], list[AOTDescriptor]],
    ) -> None:
        # unwrap a subclass into plain tensors and their size/stride if "append_symint"
        # is True
        if not is_traceable_wrapper_subclass(t):
            out[0].append(_maybe_fakeify_opaque(t))
            out[1].append(desc)
            return

        attrs, _ = t.__tensor_flatten__()

        SubclassGetAttr: Callable[[AOTInput | AOTOutput, str], AOTDescriptor]
        SubclassSize: Callable[[AOTInput | AOTOutput, int], AOTDescriptor]
        SubclassStride: Callable[[AOTInput | AOTOutput, int], AOTDescriptor]
        if isinstance(desc, AOTInput):
            SubclassGetAttr = SubclassGetAttrAOTInput  # type: ignore[bad-assignment]
            SubclassSize = SubclassSizeAOTInput  # type: ignore[bad-assignment]
            SubclassStride = SubclassStrideAOTInput  # type: ignore[bad-assignment]
        else:
            SubclassGetAttr = SubclassGetAttrAOTOutput  # type: ignore[bad-assignment]
            SubclassSize = SubclassSizeAOTOutput  # type: ignore[bad-assignment]
            SubclassStride = SubclassStrideAOTOutput  # type: ignore[bad-assignment]

        for attr in attrs:
            inner_value = getattr(t, attr)
            n_desc: Any = SubclassGetAttr(desc, attr)
            flatten_subclass(inner_value, n_desc, out=out)

        if append_symints:
            sizes = enumerate_filter_symints(t.size())
            strides = enumerate_filter_symints(t.stride())
            out[0].extend(s for _, s in sizes)
            out[0].extend(s for _, s in strides)
            out[1].extend(SubclassSize(desc, i) for i, _ in sizes)
            out[1].extend(SubclassStride(desc, i) for i, _ in strides)

    xs_inner: list[FxValue] = []
    descs_inner: list[AOTDescriptor] = []

    for x, desc in zip(wrapped_args, wrapped_args_descs):
        flatten_subclass(x, desc, out=(xs_inner, descs_inner))

    return xs_inner, descs_inner

