
def get_async_library() -> str:
    try:
        return sniffio.current_async_library()
    except Exception:
        return "false"

