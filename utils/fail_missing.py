
def fail_missing(mod: str, reason: ModuleNotFoundReason) -> None:
    if reason is ModuleNotFoundReason.NOT_FOUND:
        clarification = "(consider using --search-path)"
    elif reason is ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS:
        clarification = "(module likely exists, but is not PEP 561 compatible)"
    else:
        clarification = f"(unknown reason '{reason}')"
    raise SystemExit(f"Can't find module '{mod}' {clarification}")

