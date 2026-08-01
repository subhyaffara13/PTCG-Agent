
def get_traced_code() -> list[CodeType] | None:
    from torch._guards import TracingContext

    return TracingContext.get_traced_code()

