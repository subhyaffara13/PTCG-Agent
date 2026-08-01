
def _assert_async(cond, msg):
    cond.realize()
    cond = to_dtype(cond, torch.bool)

    def inner_fn(index):
        with ir.ComputedBuffer.force_realize():
            return ops.device_assert_async(cond.make_loader()(index), msg)

    assertion_op = Pointwise.create(
        device=cond.get_device(),
        dtype=cond.get_dtype(),
        inner_fn=inner_fn,
        ranges=list(cond.get_size()),
    )
    assertion_op.realize()
    return assertion_op

