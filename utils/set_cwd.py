
def set_cwd(path: str) -> Iterator[None]:
    old_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old_cwd)

