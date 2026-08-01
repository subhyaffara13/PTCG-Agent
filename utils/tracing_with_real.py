
def tracing_with_real(x: torch.ScriptObject) -> bool:
    if not hasattr(x, "tracing_mode"):
        return False

    if x.tracing_mode() not in ["real", "fake"]:
        raise AssertionError(
            f"tracing_mode can be either real or fake but got {x.tracing_mode()}"
        )
    return x.tracing_mode() == "real"

