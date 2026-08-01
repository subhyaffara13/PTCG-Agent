
def get_ctx() -> "torch._library.fake_impl.FakeImplCtx":
    """get_ctx() returns the current AbstractImplCtx object.

    Calling ``get_ctx()`` is only valid inside of an fake impl
    (see :func:`torch.library.register_fake` for more usage details.
    """
    return torch._library.fake_impl.global_ctx_getter()

