
def is_vision_available() -> bool:
    try:
        import PIL.Image  # noqa: F401

        return True
    except ImportError:
        return False

