
def _device_handler(args: Sequence[object]) -> torch.device:
    # NB: Don't use is_our_fake, just serve the fake information
    # as is.  Notice we don't use 'self'; we use args[0].fake_mode
    # because they may not be the same.  It would also be possible
    # to return NotImplemented here, in which case the FakeTensor
    # handler on args[0] would handle it, but we're being nice and
    # short-circuiting quickly.
    if len(args) != 1 or not isinstance(args[0], FakeTensor):
        raise AssertionError(
            "Expected exactly one FakeTensor argument for _device_handler"
        )
    if args[0].fake_mode.in_kernel_invocation:
        return torch.device("meta")
    else:
        return args[0].fake_device

