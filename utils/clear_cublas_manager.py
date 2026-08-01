
def clear_cublas_manager() -> Generator[None, None, None]:
    "Context manager around clearing cublas caches that will clear on enter and exit"
    clear_cublass_cache()
    try:
        yield
    finally:
        clear_cublass_cache()

