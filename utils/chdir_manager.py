
def chdir_manager(target: str) -> Iterator[None]:
    dir = os.getcwd()
    os.chdir(target)
    try:
        yield
    finally:
        os.chdir(dir)

