
def add_catch_all_gitignore(target_dir: str) -> None:
    """Add catch-all .gitignore to an existing directory.

    No-op if the .gitignore already exists.
    """
    gitignore = os_path_join(target_dir, ".gitignore")
    try:
        with open(gitignore, "x") as f:
            print("# Automatically created by mypy", file=f)
            print("*", file=f)
    except FileExistsError:
        pass

