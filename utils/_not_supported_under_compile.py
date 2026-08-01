
def _not_supported_under_compile(name, *, suggestion=None):
    msg = (
        f"torch.distributed.nn.functional.{name} is not supported under torch.compile."
    )
    if suggestion:
        msg += f" Use {suggestion} instead."
    raise RuntimeError(msg)

