
def get_xpu_version() -> str | None:
    # string of version, like 20250101
    try:
        xpu_version = torch.version.xpu or ""
        return xpu_version
    except Exception:
        log.exception("Error getting xpu version")
        return None

