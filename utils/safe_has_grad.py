
def safe_has_grad(t: object) -> bool:
    with torch._logging.hide_warnings(torch._logging._internal.safe_grad_filter):
        return hasattr(t, "grad")

