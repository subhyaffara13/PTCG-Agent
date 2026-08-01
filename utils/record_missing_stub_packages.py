
def record_missing_stub_packages(cache_dir: str, missing_stub_packages: set[str]) -> None:
    """Write a file containing missing stub packages.

    This allows a subsequent "mypy --install-types" run (without other arguments)
    to install missing stub packages.
    """
    fnam = missing_stubs_file(cache_dir)
    if missing_stub_packages:
        with open(fnam, "w") as f:
            for pkg in sorted(missing_stub_packages):
                f.write(f"{pkg}\n")
    else:
        if os.path.isfile(fnam):
            os.remove(fnam)

