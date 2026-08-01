
def activated_tracemalloc() -> Generator[None, None, None]:
    tracemalloc.start()
    try:
        yield
    finally:
        tracemalloc.stop()

