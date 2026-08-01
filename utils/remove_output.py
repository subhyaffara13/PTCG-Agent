
def remove_output(*sources: str) -> Iterator[None]:
    try:
        yield
    finally:
        for src in sources:
            shutil.rmtree(src)

