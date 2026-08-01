
def is_inductor_supported() -> bool:
    try:
        check_if_inductor_supported()
        return True
    except Exception:
        return False

