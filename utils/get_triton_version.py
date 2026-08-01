
def get_triton_version(fallback: tuple[int, int] = (0, 0)) -> tuple[int, int]:
    try:
        import triton

        major, minor = tuple(int(v) for v in triton.__version__.split(".")[:2])
        return (major, minor)
    except ImportError:
        return fallback

