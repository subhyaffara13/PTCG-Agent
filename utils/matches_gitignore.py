
def matches_gitignore(subpath: str, fscache: FileSystemCache, verbose: bool) -> bool:
    dir, _ = os.path.split(subpath)
    for gi_path, gi_spec in find_gitignores(dir):
        relative_path = os.path.relpath(subpath, gi_path)
        if fscache.isdir(relative_path):
            relative_path = relative_path + "/"
        if gi_spec.match_file(relative_path):
            if verbose:
                print(
                    f"TRACE: Excluding {relative_path} (matches .gitignore) in {gi_path}",
                    file=sys.stderr,
                )
            return True
    return False

