from typing import Any

def _fake_obj_from_real(fake_mode, x) -> Any:
    fake_class = _find_fake_class_for_script_object(x)

    from_real_method = getattr(fake_class, _CONVERT_FROM_REAL_NAME, None)
    if not from_real_method:
        raise RuntimeError(
            f"{fake_class} must define a classmethod {_CONVERT_FROM_REAL_NAME}"
            f" that converts the real object to the fake object."
        )

    # from_real defined by user need the ctx to fakify the tensor states.
    ctx = torch._library.fake_impl.FakeImplCtx(fake_mode, None)
    with torch._library.fake_impl.set_ctx_getter(lambda: ctx):
        return fake_class.from_real(x)

