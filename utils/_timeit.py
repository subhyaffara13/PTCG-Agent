
def _timeit(name: str) -> Generator[None, None, None]:
    start = time.perf_counter()
    yield
    dur = time.perf_counter() - start
    logger.info("%s took %ss", name, dur)

