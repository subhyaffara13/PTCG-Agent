
def find_gitignores(dir: str) -> list[tuple[str, GitIgnoreSpec]]:
    parent_dir = os.path.dirname(dir)
    if parent_dir == dir or os.path.exists(os.path.join(dir, ".git")):
        parent_gitignores = []
        git_info_exclude = os.path.join(dir, ".git", "info", "exclude")
        if os.path.isfile(git_info_exclude):
            with open(git_info_exclude) as f:
                exclude_lines = f.readlines()
            try:
                parent_gitignores = [(dir, GitIgnoreSpec.from_lines("gitignore", exclude_lines))]
            except GitIgnorePatternError:
                print(f"error: could not parse {git_info_exclude}", file=sys.stderr)
    else:
        parent_gitignores = find_gitignores(parent_dir)

    gitignore = os.path.join(dir, ".gitignore")
    if os.path.isfile(gitignore):
        with open(gitignore) as f:
            lines = f.readlines()
        try:
            return parent_gitignores + [(dir, GitIgnoreSpec.from_lines("gitignore", lines))]
        except GitIgnorePatternError:
            print(f"error: could not parse {gitignore}", file=sys.stderr)
            return parent_gitignores
    return parent_gitignores

